from __future__ import annotations

import inspect
import itertools
import math
from abc import abstractmethod, ABC
from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Iterator, Iterable

import networkx as nx
import numpy as np
import torch
import torch.nn as nn
from random_events.product_algebra import Event, SimpleEvent, VariableMap
from random_events.sigma_algebra import AbstractCompositeSet
from random_events.utils import recursive_subclasses
from random_events.variable import Variable, Continuous, Integer
from sortedcontainers import SortedSet
from typing_extensions import List, Tuple, Type, Dict, Union, Self

from ...error import IntractableError
from ..nx.probabilistic_circuit import ProbabilisticCircuit, \
    ProbabilisticCircuitMixin, SumUnit, ProductUnit
from ...probabilistic_model import ProbabilisticModel, OrderType, CenterType, MomentType
from .utils import (add_sparse_edges_dense_child_tensor_inplace,
                                       sparse_remove_rows_and_cols_where_all, shrink_index_tensor,
                                       embed_sparse_tensors_in_new_sparse_tensor, create_sparse_tensor_indices_from_row_lengths)


def inverse_class_of(clazz: Type[ProbabilisticCircuitMixin]) -> Type[Layer]:
    for subclass in recursive_subclasses(Layer):
        if not inspect.isabstract(subclass):
            if issubclass(clazz, subclass.original_class()):
                return subclass

    raise TypeError(f"Could not find class for {clazz}")


class Layer(nn.Module, ProbabilisticModel):
    """
    Abstract class for Layers of a layered circuit.

    Layers have the same scope (set of variables) for every node in them.
    """

    def mergeable_with(self, other: Layer):
        return self.variables == other.variables and type(self) == type(other)

    @property
    def support(self) -> Event:
        if self.number_of_nodes == 1:
            return self.support_per_node[0]
        raise ValueError("The support is only defined for layers with one node. Use the support_per_node property "
                         "if you want the support of each node.")

    @property
    @abstractmethod
    def support_per_node(self) -> List[Event]:
        """
        :return: The support of each node in the layer as a list of events.
        """
        raise NotImplementedError

    @property
    def deterministic(self) -> torch.BoolTensor:
        """
        :return: Rather, the layer is deterministic for each node as a boolean tensor.
        """
        raise NotImplementedError

    @property
    def is_root(self) -> bool:
        """
        :return: Whether the layer is a possible root layer of the circuit.
        """
        return self.number_of_nodes == 1

    @classmethod
    def original_class(cls) -> Tuple[Type, ...]:
        """
        :return: The tuple of matching classes of the layer in the probabilistic_model.probabilistic_circuit package.
        """
        return tuple()

    @property
    @abstractmethod
    def variables(self) -> Tuple[Variable, ...]:
        """
        :return: The variables of the layer.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_smooth(self) -> torch.Tensor:
        """
        :return: A bool tensor that indicates if a node is smooth or not with shape (#nodes).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_decomposable(self) -> torch.Tensor:
        """
        :return: A bool tensor that indicates if a node is decomposable or not with shape (#nodes).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_deterministic(self) -> torch.Tensor:
        """
        :return: A bool tensor that indicates if a node is deterministic or not with shape (#nodes).
        """
        raise NotImplementedError

    @property
    def numeric_variables(self) -> Tuple[Variable, ...]:
        return tuple(v for v in self.variables if isinstance(v, (Continuous, Integer)))

    @abstractmethod
    def validate(self):
        """
        Validate the parameters and their layouts.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def number_of_nodes(self) -> int:
        """
        :return: The number of nodes in the layer.
        """
        raise NotImplementedError

    def log_likelihood(self, events: np.ndarray) -> torch.Tensor:
        if isinstance(events, np.ndarray):
            events = torch.from_numpy(events)

        ll = self.log_likelihood_of_nodes(events)
        return ll.numpy()

    @abstractmethod
    def log_likelihood_of_nodes(self, x: torch.Tensor) -> torch.Tensor:
        """
        Calculate the log-likelihood of the distribution.

        .. note::
            The shape of the log likelihood depends on the number of samples and nodes.
            The shape of the result is (#samples, #nodes).
            The first dimension indexes the samples, the second the nodes.
        """
        raise NotImplementedError

    def probability_of_simple_event(self, event: SimpleEvent) -> torch.DoubleTensor:
        """
        Calculate the probability of a simple event.
        :param event: The simple event.
        :return: The probability of the event for each node in the layer.
        The result is a double tensor with shape (#nodes,).
        """
        raise NotImplementedError

    def log_mode(self) -> Tuple[Event, float]:
        assert self.is_root
        modes, ll = self.log_mode_of_nodes()
        return modes[0], ll.item()

    @abstractmethod
    def log_mode_of_nodes(self) -> Tuple[List[Event], torch.Tensor]:
        """
        Calculate the mode and logarithmic maximum for every node.

        :return: A list of events representing the argmax, and a tensor representing the log max for every node.
                The shapes for both are (#nodes).
        """
        raise NotImplementedError

    @staticmethod
    def from_probabilistic_circuit(pc: ProbabilisticCircuit) -> Layer:
        """
        Convert a probabilistic circuit to a layered circuit.
        The result expresses the same distribution as `pc`.

        :param pc: The probabilistic circuit.
        :return: The layered circuit.
        """

        node_to_depth_map = {node: nx.shortest_path_length(pc, pc.root, node) for node in pc.nodes}
        layer_to_nodes_map = {depth: [node for node, n_depth in node_to_depth_map.items() if depth == n_depth] for depth
                              in set(node_to_depth_map.values())}
        child_layers = []

        for layer_index, nodes in reversed(layer_to_nodes_map.items()):
            child_layers = Layer.create_layers_from_nodes(nodes, child_layers)
        return child_layers[0].layer

    @staticmethod
    def create_layers_from_nodes(nodes: List[ProbabilisticCircuitMixin], child_layers: List[AnnotatedLayer]) \
            -> List[AnnotatedLayer]:
        """
        Create a layer from a list of nodes.
        """
        result = []

        unique_types = set(type(node) for node in nodes)
        for unique_type in unique_types:
            nodes_of_current_type = [node for node in nodes if isinstance(node, unique_type)]
            layer_type = inverse_class_of(unique_type)
            scopes = [tuple(node.variables) for node in nodes_of_current_type]
            unique_scopes = set(scopes)
            for scope in unique_scopes:
                nodes_of_current_type_and_scope = [node for node in nodes_of_current_type if
                                                   tuple(node.variables) == scope]
                layer = layer_type.create_layer_from_nodes_with_same_type_and_scope(nodes_of_current_type_and_scope,
                                                                                    child_layers)
                result.append(layer)

        return result

    @classmethod
    @abstractmethod
    def create_layer_from_nodes_with_same_type_and_scope(cls, nodes: List[ProbabilisticCircuitMixin],
                                                         child_layers: List[AnnotatedLayer]) -> \
            AnnotatedLayer:
        """
        Create a layer from a list of nodes with the same type and scope.
        """
        raise NotImplementedError

    def log_conditional(self, event: Event) -> Tuple[Optional[Layer], float]:
        if event.is_empty():
            conditional, log_prob = self.impossible_condition_result
        elif len(event.simple_sets) == 1:
            conditional, log_prob = self.log_conditional_of_simple_event(event.simple_sets[0])
        else:
            conditional, log_prob = self.log_conditional_of_composite_event(event)
        return conditional, log_prob.item()

    def log_conditional_of_composite_event(self, event: Event) -> Tuple[Optional[Layer], torch.Tensor]:
        """
        :param event: The composite event.
        :return: The conditional distribution and the log probability of the event.
        The log probability is a double tensor with shape (#nodes,).
        """
        # get conditionals of each simple event
        results = [self.log_conditional_of_simple_event(simple_event) for simple_event in event.simple_sets]

        # filter valid input layers
        possible_layers = [(layer, ll) for layer, ll in results if layer is not None]

        # if the result is impossible, return it
        if len(possible_layers) == 0:
            return self.impossible_condition_result

        # create new log weights and new layers inefficiently TODO: some merging of layers if possible
        log_weights = [torch.sparse_coo_tensor(torch.tensor([[0], [0]]), ll) for _, ll in possible_layers]
        layers = [layer for layer, _ in possible_layers]
        # construct result
        resulting_layer = SumLayer(layers, log_weights)

        # calculate log probability
        log_prob = resulting_layer.log_normalization_constants

        return resulting_layer, log_prob

    @abstractmethod
    def log_conditional_of_simple_event(self, event: SimpleEvent) -> Tuple[Optional[Layer], torch.Tensor]:
        """
        :param event: The simple event.
        :return: The conditional distribution and the log probability of the event.
        The log probability is a double tensor with shape (#nodes,).
        """
        raise NotImplementedError

    @abstractmethod
    def merge_with(self, others: List[Self]):
        """
        Merge this layer with another layer inplace.

        :param others: The other layers
        """
        raise NotImplementedError

    @property
    def impossible_condition_result(self) -> Tuple[None, torch.Tensor]:
        """
        :return: The result that a layer yields if it is conditioned on an event E with P(E) = 0
        """
        return None, torch.full((self.number_of_nodes,), -torch.inf, dtype=torch.double)

    @abstractmethod
    def remove_nodes_inplace(self, remove_mask: torch.BoolTensor):
        """
        Remove nodes from the layer inplace.

        Also updates possible child layers if needed.

        :param remove_mask: The mask that indicates which nodes to remove.
        True indicates that the node should be removed.
        """
        raise NotImplementedError

    def __deepcopy__(self):
        raise NotImplementedError

    def sample(self, amount: int) -> np.array:
        samples = self.sample_from_frequencies(torch.tensor([amount]))[0].to_dense()
        return samples.numpy()

    def sample_from_frequencies(self, frequencies: torch.Tensor) -> torch.Tensor:
        """
        Sample from the layer.
        The frequencies are used to determine the number of samples that should be drawn for each node.

        :param frequencies: The frequencies for each node as LongTensor with shape (#nodes,).
        :return: The samples with shape (#samples, #nodes).
        """
        raise NotImplementedError

    def cdf(self, events: Union[np.array, torch.Tensor]) -> np.array:
        """
        ..Note:: This will try to remove the node dimension of the layer. Use `cdf_of_nodes` if you want the cdf
        for every node.
        """
        if isinstance(events, np.ndarray):
            events = torch.from_numpy(events)
        cdf = self.cdf_of_nodes(events)
        return cdf.squeeze()

    def cdf_of_nodes(self, events: torch.Tensor) -> torch.Tensor:
        """
        Calculate the cdf of each node in this layer for every event in ``events``.
        :param events: The events to calculate the cdf for
        :return: The cdf of every event for every node with shape (#events, #nodes)
        """
        raise NotImplementedError

    def moment(self, order: OrderType, center: CenterType) -> MomentType:
        order_and_center = torch.tensor([[order[v], center[v]] if v.is_numeric else [0, 0] for v in self.variables])
        moment = self.moment_of_nodes(order_and_center[:, 0].long(), order_and_center[:, 1].double())
        return VariableMap({v: m.item() for v, m in zip(self.variables, moment[0]) if v.is_numeric})

    def moment_of_nodes(self, order: torch.Tensor, center: torch.Tensor) -> torch.Tensor:
        """
        Calculate the moments of all continuous/integer variables.

        :param order: The order of the moment for each variable of this layer as long tensor with shape (#variables,).
        :param center: The center of the moment for each variable of this layer as float tensor with shape (#variables,).
        :return: The moment of each node for each variable of this layer with shape (#nodes, #variables).
        """
        raise NotImplementedError


class InnerLayer(Layer, ABC):
    """
    Abstract Base Class for inner layers
    """

    child_layers: List[Layer]
    """
    The child layers of this layer.
    """

    def __init__(self, child_layers: List[Layer]):
        super().__init__()
        self.child_layers = child_layers

    @cached_property
    def variables(self) -> Tuple[Variable, ...]:
        return tuple(sorted(set().union(*[child_layer.variables for child_layer in self.child_layers])))


class InputLayer(Layer, ABC):
    """
    Abstract base class for univariate input units.

    Input layers contain only one type of distribution such that the vectorization of the log likelihood
    calculation works without bottleneck statements like if/else or loops.
    """

    variable: Variable
    """
    The variable of the distributions.
    """

    def __init__(self, variable: Variable):
        super().__init__()
        self.variable = variable

    @property
    def variables(self) -> Tuple[Variable, ...]:
        return self.variable,

    @property
    def support_per_node(self) -> List[Event]:
        return [SimpleEvent({self.variable: us}).as_composite_set()
                for us in self.univariate_support_per_node]

    @property
    @abstractmethod
    def univariate_support_per_node(self) -> List[AbstractCompositeSet]:
        """
        The univariate support of the layer for each node.
        """
        raise NotImplementedError

    @cached_property
    def is_decomposable(self) -> torch.Tensor:
        return torch.ones(self.number_of_nodes, dtype=torch.bool)

    @cached_property
    def is_smooth(self) -> torch.Tensor:
        return torch.ones(self.number_of_nodes, dtype=torch.bool)

    @cached_property
    def is_deterministic(self) -> torch.Tensor:
        return torch.ones(self.number_of_nodes, dtype=torch.bool)

    def marginal(self, variables: Iterable[Variable]) -> Optional[Self]:
        if self.variable in variables:
            return self
        return None


class SumLayer(InnerLayer):
    """
    A layer that represents the sum of multiple other layers.
    """

    child_layers: Union[List[[ProductLayer]], List[InputLayer]]
    """
    Child layers of the sum unit. 
            
    Smoothness Requires that all sums go over the same scope. Hence the child layers have to have the same scope.
    
    In a smooth sum unit the child layers are 
        - product layers if the sum is multivariate
        - input layers if the sum is univariate
    """

    log_weights: List[torch.Tensor]
    """
    The sparse logarithmic weights of each edge.
    The list consists of tensor that are interpreted as weights for each child layer.
    
    The first dimension of each tensor must match the number of nodes of this layer and hence has to be 
    constant.
    The second dimension of each tensor must match the number of nodes of the  respective child layer.
    
    The weights are normalized per row.
    Each weight tensor is of type double.
    """

    def __init__(self, child_layers: List[Layer], log_weights: List[torch.Tensor]):
        """
        Initialize the sum layer.

        :param child_layers: The child layers of the sum layer.
        :param log_weights: The logarithmic weights of each edge.
        """
        super().__init__(child_layers)
        self.log_weights = log_weights

    def validate(self):
        for log_weights in self.log_weights:
            assert log_weights.shape[0] == self.number_of_nodes, "The number of nodes must match the number of weights."

        for log_weights, child_layer in self.log_weighted_child_layers:
            assert log_weights.shape[
                       1] == child_layer.number_of_nodes, "The number of nodes must match the number of weights."

    @classmethod
    def original_class(cls) -> Tuple[Type, ...]:
        return SumUnit,

    @property
    def log_weighted_child_layers(self) -> Iterator[Tuple[torch.Tensor, Union[ProductLayer, InputLayer]]]:
        """
        :returns: Yields log weights and the child layers zipped together.
        """
        yield from zip(self.log_weights, self.child_layers)

    @property
    def concatenated_log_weights(self) -> torch.Tensor:
        """
        :return: The concatenated weights of the child layers for each node.
        """
        return torch.cat(self.log_weights, dim=1)

    @property
    def log_normalization_constants(self) -> torch.Tensor:
        result = self.concatenated_log_weights.clone().coalesce()
        result.values().exp_()
        result = result.sum(1)
        result.values().log_()
        return result.to_dense()

    @property
    def normalized_log_weights(self):
        result = [log_weights.clone().coalesce() for log_weights in self.log_weights]
        log_normalization_constants = self.log_normalization_constants
        for log_weights in result:
            log_weights.values().sub_(log_normalization_constants[log_weights.indices()[0]])
        return result

    @cached_property
    def is_decomposable(self) -> torch.Tensor:
        return torch.ones(self.number_of_nodes, dtype=torch.bool)

    @cached_property
    def is_smooth(self) -> torch.Tensor:
        for child_layer in self.child_layers:
            if child_layer.variables != self.variables:
                return torch.zeros(self.number_of_nodes, dtype=torch.bool)
        return torch.ones(self.number_of_nodes, dtype=torch.bool)

    @cached_property
    def is_deterministic(self) -> torch.Tensor:
        result = torch.ones(self.number_of_nodes, dtype=torch.bool)
        child_layer_supports = [supp for layer in self.child_layers for supp in layer.support_per_node]  #

        for node, node_log_weights in enumerate(self.concatenated_log_weights):
            node_log_weights = node_log_weights.coalesce()

            # get supports for this node
            relevant_supports = [child_layer_supports[index] for index, log_weight in
                                 zip(node_log_weights.indices()[0], node_log_weights.values())
                                 if log_weight > -torch.inf]

            # check if the supports intersect somewhere
            for support_a, support_b in itertools.combinations(relevant_supports, 2):
                if not support_a.intersection_with(support_b).is_empty():
                    result[node] = False
                    break

        return result

    @property
    def concatenated_normalized_weights(self) -> torch.Tensor:
        result = self.concatenated_log_weights.coalesce()
        log_z = self.log_normalization_constants
        result.values().sub_(log_z[result.indices()[0]])
        result.values().exp_()
        return result.coalesce()

    @property
    def number_of_nodes(self) -> int:
        return self.log_weights[0].shape[0]

    @cached_property
    def support_per_node(self) -> List[Event]:
        result = [Event() for _ in range(self.number_of_nodes)]
        for log_weights, child_layer in self.log_weighted_child_layers:
            for node, log_weights_of_node in enumerate(log_weights):
                log_weights_of_node = log_weights_of_node.coalesce()
                for child_idx, log_prob in zip(log_weights_of_node.indices()[0], log_weights_of_node.values()):
                    if log_prob > -torch.inf:
                        result[node] |= child_layer.support_per_node[child_idx]
        return result

    @classmethod
    def create_layer_from_nodes_with_same_type_and_scope(cls, nodes: List[SumUnit],
                                                         child_layers: List[AnnotatedLayer]) -> \
            AnnotatedLayer:

        result_hash_remap = {hash(node): index for index, node in enumerate(nodes)}
        variables = tuple(nodes[0].variables)
        number_of_nodes = len(nodes)

        # filter the child layers to only contain layers with the same scope as this one
        filtered_child_layers = [child_layer for child_layer in child_layers if tuple(child_layer.layer.variables) ==
                                 variables]
        log_weights = []

        # for every possible child layer
        for child_layer in filtered_child_layers:

            # initialize indices and values for sparse weight matrix
            indices = []
            values = []

            # gather indices and log weights
            for index, node in enumerate(nodes):
                for weight, subcircuit in node.weighted_subcircuits:
                    if hash(subcircuit) in child_layer.hash_remap:
                        indices.append((index, child_layer.hash_remap[hash(subcircuit)]))
                        values.append((math.log(weight)))

            # assemble sparse log weight matrix
            log_weights.append(torch.sparse_coo_tensor(torch.tensor(indices).T,
                                                       torch.tensor(values, dtype=torch.double),
                                                       (number_of_nodes, child_layer.layer.number_of_nodes),
                                                       is_coalesced=True))

        sum_layer = cls([cl.layer for cl in filtered_child_layers], log_weights)
        return AnnotatedLayer(sum_layer, nodes, result_hash_remap)

    def probability_of_simple_event(self, event: SimpleEvent) -> torch.Tensor:
        result = torch.zeros(self.number_of_nodes, 1)
        for log_weights, child_layer in self.log_weighted_child_layers:
            child_layer_prob = child_layer.probability_of_simple_event(event)  # shape: (#child_nodes, 1)
            weights = (torch.exp(log_weights - self.log_normalization_constants.unsqueeze(-1)).
                       to(child_layer_prob.dtype))  # shape: (#nodes, #child_nodes)
            probabilities = torch.matmul(weights, child_layer_prob)
            result += probabilities
        return result

    def log_mode_of_nodes(self) -> Tuple[List[Event], torch.Tensor]:
        if not self.is_deterministic.all():
            raise IntractableError("The mode of a layer that contains non-deterministic sum units is intractable.")

        # initialize results
        result_ll = torch.full((self.number_of_nodes,), torch.nan, dtype=torch.double)
        result_mode = [Event() for _ in range(self.number_of_nodes)]

        # calculate and organize the child layer results
        child_layer_results = [layer.log_mode_of_nodes() for layer in self.child_layers]
        child_layer_modes = [mode for modes, _ in child_layer_results for mode in modes]
        concatenated_log_max = torch.cat([log_max for _, log_max in child_layer_results])
        normalized_log_weights = torch.cat(self.normalized_log_weights, dim=1).coalesce()

        # weight the log maxima
        normalized_log_weights.values().add_(concatenated_log_max[normalized_log_weights.indices()[1]])

        for node, log_maxima in enumerate(normalized_log_weights):
            log_maxima = log_maxima.coalesce()
            # calculate maximum
            log_maxima_values = log_maxima.values()
            log_max = log_maxima_values.max()
            result_ll[node] = log_max

            # merge modes
            maxima_indices = (log_maxima_values == log_max).nonzero().squeeze(0)
            for index in maxima_indices:
                result_mode[node] |= child_layer_modes[log_maxima.indices()[0, index]]

        return result_mode, result_ll

    def __deepcopy__(self):
        child_layers = [child_layer.__deepcopy__() for child_layer in self.child_layers]
        log_weights = [log_weight.clone() for log_weight in self.log_weights]
        return self.__class__(child_layers, log_weights)

    def mergeable_layer_matrix(self, other: Self) -> torch.Tensor:
        """
        Create a matrix that describes which child layers of this layer can be merged with which child layers of the
        other layer.

        The entry [i, j] is True if the i-th child layer of this layer can be merged with the j-th child layer of the
        other layer.

        :param other: The other layer.
        :return: The mergeable boolean matrix
        """

        # create matrix describing mergeable layers
        mergeable_matrix = torch.zeros((len(self.child_layers), len(other.child_layers)), dtype=torch.bool)

        # fill matrix
        for i, layer in enumerate(self.child_layers):
            for j, other_layer in enumerate(other.child_layers):
                mergeable_matrix[i, j] = layer.mergeable_with(other_layer)
        return mergeable_matrix

    def merge_with_one_layer_inplace(self, other: Self):
        """
        Merge this layer with another layer inplace.

        :param other: The other layer

        """

        mergeable_matrix = self.mergeable_layer_matrix(other)
        assert (mergeable_matrix.sum(dim=1) <= 1).all(), "There must be at most one mergeable layer per layer."

        total_number_of_nodes = self.number_of_nodes + other.number_of_nodes
        new_layers = []
        new_log_weights = []

        for log_weights, layer, mergeable_row in zip(self.log_weights, self.child_layers, mergeable_matrix):

            # if this layer cant be merged with any other layer
            if mergeable_row.sum() == 0:
                # append impossible log weights to match the new number of nodes
                log_weights = torch.sparse_coo_tensor(log_weights.indices(), log_weights.values(),
                                                      (total_number_of_nodes, layer.number_of_nodes),
                                                      dtype=torch.double, is_coalesced=True)

                new_layers.append(layer)
                new_log_weights.append(log_weights)
                continue

            # filter for the mergeable layers
            mergeable_other_layers = [other_layer for other_layer, mergeable
                                      in zip(other.child_layers, mergeable_row) if mergeable]

            # filter for the mergeable log_weights
            mergeable_log_weights = [log_weights] + [other_log_weights for other_log_weights, mergeable
                                                     in zip(other.log_weights, mergeable_row) if mergeable]

            # merge the log_weights
            embedded_log_weights = embed_sparse_tensors_in_new_sparse_tensor(mergeable_log_weights)
            new_log_weights.append(embedded_log_weights)

            # merge the layers
            layer.merge_with(mergeable_other_layers)
            new_layers.append(layer)

        # check if any child_layer from the other layer has not been merged
        for other_log_weights, other_layer, mergeable_col in zip(other.log_weights, other.child_layers,
                                                                 mergeable_matrix.T):
            if mergeable_col.sum() == 0:
                # append impossible log weights to match the new number of nodes
                other_log_weights = torch.sparse_coo_tensor(other_log_weights.indices(), other_log_weights.values(),
                                                            (total_number_of_nodes, other_layer.number_of_nodes),
                                                            dtype=torch.double, is_coalesced=True)
                new_log_weights.append(other_log_weights)
                new_layers.append(other_layer)

        self.log_weights = new_log_weights
        self.child_layers = new_layers

    def merge_with(self, others: List[Self]):
        [self.merge_with_one_layer_inplace(other) for other in others]

    def log_likelihood_of_nodes(self, x: torch.Tensor) -> torch.Tensor:
        result = torch.zeros(len(x), self.number_of_nodes, dtype=torch.double)

        for log_weights, child_layer in self.log_weighted_child_layers:
            # get the log likelihoods of the child nodes
            ll = child_layer.log_likelihood_of_nodes(x)
            # assert ll.shape == (len(x), child_layer.number_of_nodes)

            # weight the log likelihood of the child nodes by the weight for each node of this layer
            cloned_log_weights = log_weights.clone()  # clone the weights
            cloned_log_weights.values().exp_()  # exponent weights
            ll = ll.exp()  # calculate the exponential of the child log likelihoods
            #  calculate the weighted sum in layer
            ll = torch.matmul(ll, cloned_log_weights.T)

            # sum the child layer result
            result += ll

        return torch.log(result) - self.log_normalization_constants

    def cdf_of_nodes(self, events: torch.Tensor) -> torch.Tensor:
        result = torch.zeros(len(events), self.number_of_nodes, dtype=torch.double)

        for log_weights, child_layer in self.log_weighted_child_layers:
            # get the cdf of the child nodes
            cdf = child_layer.cdf_of_nodes(events)

            # weight the cdf of the child nodes by the weight for each node of this layer
            cloned_weights = log_weights.clone()  # clone the weights
            cloned_weights.values().exp_()  # exponent weights

            #  calculate the weighted sum in layer
            cdf = torch.matmul(cdf, cloned_weights.T)

            # sum the child layer result
            result += cdf

        return result / torch.exp(self.log_normalization_constants)

    def remove_nodes_inplace(self, remove_mask: torch.BoolTensor):
        keep_mask = ~remove_mask
        keep_indices = keep_mask.nonzero().squeeze(-1)

        # initialize new log weights and child_layers
        new_log_weights = []
        new_child_layers = []

        for log_weights, child_layer in self.log_weighted_child_layers:

            # remove nodes (rows)
            log_weights = log_weights.index_select(0, keep_indices).coalesce()

            # calculate probabilities of child layer nodes
            child_layer_probabilities = log_weights.clone().coalesce()
            child_layer_probabilities = child_layer_probabilities.sum(0)  # shape: (#child_nodes,)
            child_layer_probabilities.values().exp_()
            child_layer_probabilities = child_layer_probabilities.to_dense()

            # check if there is a child that has no incoming edge anymore
            remove_mask: torch.BoolTensor = child_layer_probabilities == 0
            if remove_mask.any():
                child_layer.remove_nodes_inplace(remove_mask)

            if child_layer.number_of_nodes > 0:
                new_log_weights.append(sparse_remove_rows_and_cols_where_all(log_weights, -torch.inf))
                new_child_layers.append(child_layer)

        self.log_weights = new_log_weights
        self.child_layers = new_child_layers

    def log_conditional_of_simple_event(self, event: SimpleEvent) -> Tuple[Optional[Layer], torch.Tensor]:

        conditional_child_layers = []
        conditional_log_weights = []

        probabilities = torch.zeros(self.number_of_nodes, dtype=torch.double)

        for log_weights, child_layer in self.log_weighted_child_layers:

            # get the conditional of the child layer, log prob shape: (#child_nodes, 1)
            conditional, child_log_prob = child_layer.log_conditional_of_simple_event(event)

            if conditional is None:
                continue

            # clone weights
            log_weights = log_weights.clone().coalesce().double()  # shape: (#nodes, #child_nodes)

            # calculate the weighted sum of the child log probabilities
            add_sparse_edges_dense_child_tensor_inplace(log_weights, child_log_prob)

            # calculate the probabilities of the child nodes in total
            current_probabilities = log_weights.clone().coalesce()
            current_probabilities.values().exp_()
            current_probabilities = current_probabilities.sum(1).to_dense()
            probabilities += current_probabilities

            # update log weights for conditional layer
            log_weights = sparse_remove_rows_and_cols_where_all(log_weights, -torch.inf)

            conditional_child_layers.append(conditional)
            conditional_log_weights.append(log_weights)

        if len(conditional_child_layers) == 0:
            return self.impossible_condition_result

        resulting_layer = SumLayer(conditional_child_layers, conditional_log_weights)
        return resulting_layer, (probabilities.log() - self.log_normalization_constants)

    def sample_from_frequencies(self, frequencies: torch.Tensor) -> torch.Tensor:
        """
        Sample from the layer.
        The frequencies are used to determine the number of samples that should be drawn for each node.

        For sum nodes, this method has two stages.

        The first consists in sampling the latent variable of the sum node.
        Be aware that this step does not invoke real sampling but uses a central limit argument to produce the expected
        population. In other words, we don't sample because we know the marginal likelihood of the latent distribution.

        The second stage consists in sampling the child nodes of the sum node and assembling the samples.
        For the second stage, check the method `assemble_samples_from_node_to_child_frequency_map`.

        :param frequencies: The frequencies for each node as LongTensor with shape (#nodes,).
        :return: The samples with shape (#samples, #nodes).
        """

        # calculate the probabilities for the latent variable interpretation of this layer
        catted_weights = self.concatenated_normalized_weights

        # pseudo sample the latent variables by evaluating the events w. r. t. their probabilities (histogram)
        node_to_child_frequency_map = (catted_weights * frequencies.unsqueeze(-1)).coalesce()

        # Round the sample counts to integers.
        # This rounding is the only bias introduced into this form of sampling.
        # The bias is negligible for large sample counts.
        node_to_child_frequency_map.coalesce().values().round_()

        return self.assemble_samples_from_node_to_child_frequency_map(node_to_child_frequency_map.long())

    def assemble_samples_from_node_to_child_frequency_map(self,
                                                          node_to_child_frequency_map: torch.Tensor) -> torch.Tensor:
        """
        Assemble the samples from the frequencies of the child layers.

        :param node_to_child_frequency_map: A parse tensor that maps the nodes of this layer to the frequencies of the
        child layer nodes. An element at position (i, j) describes that node i of this layer request
        node_to_child_frequency_map[i, j] many samples from the child node j.

        :return: The samples for this layer. The result is a sparse matrix with shape
        (#nodes, max(node_to_frequency_map.sum(1)).
        """
        # offset for shifting through the frequencies of the node_to_child_frequency_map
        prev_column_index = 0

        all_samples = []

        for child_layer in self.child_layers:
            # get the block of frequencies for the child layer, shape (#nodes, #child_nodes)
            current_frequency_block = (node_to_child_frequency_map.
                                       index_select(dim=1,
                                                    index=torch.arange(prev_column_index,
                                                                       prev_column_index + child_layer.number_of_nodes))).coalesce()

            # sample the child layer w. r. t. the sample frequencies
            frequencies_for_child_nodes = current_frequency_block.sum(0).to_dense()

            # if no samples should be taken, skip this iteration
            if all(frequencies_for_child_nodes == 0):
                prev_column_index += child_layer.number_of_nodes
                continue

            # calculate total samples requested for each node of this layer
            frequencies = current_frequency_block.sum(1).to_dense()

            # calculate the row (node) in this layer the samples in samples_from_child_layer.values() belong to.
            # the node_ownership should contain the node index in this layer for each sample
            # Example: [1, 1, 0] means that the first two samples belong to node 1 and the last sample belongs to node 0.
            node_ownership = current_frequency_block.indices()[1].repeat_interleave(current_frequency_block.T.
                                                                                    coalesce().values())

            # sample the child layer
            samples_from_child_layer = child_layer.sample_from_frequencies(frequencies_for_child_nodes)

            # reorder the samples to match the node_ownership
            argsort_indices = torch.argsort(node_ownership)
            reordered_by_row_index = samples_from_child_layer.values()[argsort_indices]

            # create the transposed indices for the sparse tensor containing the samples described from this layer
            indices = create_sparse_tensor_indices_from_row_lengths(frequencies)

            # create the sparse samples for this block of nodes
            samples_of_node_block = torch.sparse_coo_tensor(indices, reordered_by_row_index,
                                                            (self.number_of_nodes, max(frequencies),
                                                             len(self.variables)), is_coalesced=True)

            all_samples.append(samples_of_node_block)

            # shift the offset
            prev_column_index += child_layer.number_of_nodes

        # concatenate the samples
        samples = torch.cat(all_samples, 1).coalesce().values()

        # calculate the total number of samples for each node
        total_frequency = node_to_child_frequency_map.sum(1).to_dense()

        # calculate the cleaned indices for the resulting tensor
        new_indices = create_sparse_tensor_indices_from_row_lengths(total_frequency)

        return torch.sparse_coo_tensor(new_indices, samples, is_coalesced=True,
                                       size=(self.number_of_nodes, max(total_frequency), len(self.variables)))

    def moment_of_nodes(self, order: torch.Tensor, center: torch.Tensor) -> torch.Tensor:
        result = torch.zeros(self.number_of_nodes, len(self.variables), dtype=torch.double)

        for log_weights, child_layer in self.log_weighted_child_layers:
            # get the moment of the child nodes
            moment = child_layer.moment_of_nodes(order, center)  # shape (#child_layer_nodes, #variables)

            # weight the moment of the child nodes by the weight for each node of this layer
            weights = log_weights.clone()  # clone the weights, shape (#nodes, #child_layer_nodes)
            weights.values().exp_()  # exponent weights

            #  calculate the weighted sum in layer
            moment = torch.matmul(weights, moment)

            # sum the child layer result
            result += moment

        return result / torch.exp(self.log_normalization_constants.unsqueeze(-1))

    def marginal(self, variables: Iterable[Variable]) -> Optional[Self]:
        if all(variable not in variables for variable in self.variables):
            return None
        marginal_child_layers = [layer.marginal(variables) for layer in self.child_layers]
        return self.__class__(marginal_child_layers, self.log_weights)



class ProductLayer(InnerLayer):
    """
    A layer that represents the product of multiple other units.
    """

    child_layers: List[Union[SumLayer, InputLayer]]
    """
    The child of a product layer is a list that contains groups sum units with the same scope or groups of input
    units with the same scope.
    """

    edges: torch.Tensor  # SparseTensor[int]
    """
    The edges consist of a sparse matrix containing integers.
    The first dimension describes the edges for each child layer.
    The second dimension describes the edges for each node in the child layer.
    The integers are interpreted in such a way that n-th value represents a edge (n, edges[n]).
    
    Nodes in the child layer can be mapped to by multiple nodes in this layer.
    
    The shape is (#child_layers, #nodes).
    """

    def __init__(self, child_layers: List[Layer], edges: torch.Tensor):
        """
        Initialize the product layer.

        :param child_layers: The child layers of the product layer.
        :param edges: The edges of the product layer.
        """
        super().__init__(child_layers)
        self.edges = edges

    def validate(self):
        assert self.edges.shape == (len(self.child_layers), self.number_of_nodes), \
            (f"The shape of the edges must be {(len(self.child_layers), self.number_of_nodes)} "
             f"but was {self.edges.shape}.")

    @classmethod
    def original_class(cls) -> Tuple[Type, ...]:
        return ProductUnit,

    @property
    def number_of_nodes(self) -> int:
        return self.edges.shape[1]

    @cached_property
    def is_decomposable(self) -> torch.Tensor:

        # create a matrix that counts which node partitions how
        variable_containment_counts = torch.zeros(self.number_of_nodes, len(self.variables), dtype=torch.long)

        for columns, edges, layer in zip(self.columns_of_child_layers, self.edges, self.child_layers):
            edges = edges.coalesce()

            # count how often variables occur for every node
            variable_containment_counts[edges.indices()[0], columns] += 1

        # check that every variable occurs exactly 1 time for every node
        result = (variable_containment_counts == 1).all(dim=1)
        return result

    @cached_property
    def is_smooth(self) -> torch.Tensor:
        return torch.ones(self.number_of_nodes, dtype=torch.bool)

    @cached_property
    def is_deterministic(self) -> torch.Tensor:
        return torch.ones(self.number_of_nodes, dtype=torch.bool)

    def decomposes_as(self, other: Layer) -> bool:
        return set(child_layer.variables for child_layer in self.child_layers) == \
            set(child_layer.variables for child_layer in other.child_layers)

    def mergeable_with(self, other: Layer):
        return super().mergeable_with(other) and self.decomposes_as(other)

    @cached_property
    def columns_of_child_layers(self) -> Tuple[Tuple[int, ...], ...]:
        """
        :return: The indices of the variables for each child layer in the variable-vector of this layer.
        """
        result = []
        for layer in self.child_layers:
            layer_indices = [self.variables.index(variable) for variable in layer.variables]
            result.append(tuple(layer_indices))
        return tuple(result)

    # @torch.compile
    def log_likelihood_of_nodes(self, x: torch.Tensor) -> torch.Tensor:
        result = torch.zeros(len(x), self.number_of_nodes, dtype=torch.double)
        for columns, edges, layer in zip(self.columns_of_child_layers, self.edges, self.child_layers):
            edges = edges.coalesce()
            # calculate the log likelihood over the columns of the child layer
            ll = layer.log_likelihood_of_nodes(x[:, columns])  # shape: (#x, #child_nodes)

            # gather the ll at the indices of the nodes that are required for the edges
            ll = ll[:, edges.values()]  # shape: (#x, #len(edges.values()))
            # assert ll.shape == (len(x), len(edges.values()))

            # add the gathered values to the result where the edges define the indices
            result[:, edges.indices().squeeze(0)] += ll

        return result

    def log_mode_of_nodes(self) -> Tuple[List[Event], torch.Tensor]:
        result_ll = torch.zeros(self.number_of_nodes, dtype=torch.double)
        result_modes = [self.universal_simple_event().as_composite_set() for _ in range(self.number_of_nodes)]

        for node, (edges, layer) in enumerate(zip(self.edges, self.child_layers)):
            edges = edges.coalesce()
            layer_modes, layer_ll = layer.log_mode_of_nodes()
            result_ll[edges.indices()[0]] += layer_ll[edges.values()]
            for edge_index, edge_value in zip(edges.indices()[0], edges.values()):
                result_modes[edge_index] &= layer_modes[edge_value]

        return result_modes, result_ll

    @classmethod
    def create_layer_from_nodes_with_same_type_and_scope(cls, nodes: List[ProductUnit],
                                                         child_layers: List[AnnotatedLayer]) -> \
            AnnotatedLayer:
        hash_remap = {hash(node): index for index, node in enumerate(nodes)}
        number_of_nodes = len(nodes)

        edge_indices = []
        edge_values = []

        # for every node in the nodes for this layer
        for node_index, node in enumerate(nodes):

            # for every child layer
            for child_layer_index, child_layer in enumerate(child_layers):

                cl_variables = SortedSet(child_layer.layer.variables)

                # for every subcircuit
                for subcircuit_index, subcircuit in enumerate(node.subcircuits):
                    # if the scopes are compatible
                    if cl_variables == subcircuit.variables:
                        # add the edge
                        edge_indices.append([child_layer_index, node_index])
                        edge_values.append(child_layer.hash_remap[hash(subcircuit)])

        # assemble sparse edge tensor
        edges = torch.sparse_coo_tensor(indices=torch.tensor(edge_indices, dtype=torch.long).T,
                                        values=torch.tensor(edge_values, dtype=torch.long)).coalesce()

        layer = cls([cl.layer for cl in child_layers], edges)
        return AnnotatedLayer(layer, nodes, hash_remap)

    def probability_of_simple_event(self, event: SimpleEvent) -> torch.Tensor:

        # initialize the result
        result = torch.ones(self.number_of_nodes, dtype=torch.double)

        for edges, layer in zip(self.edges, self.child_layers):
            edges = edges.coalesce()

            # calculate the probabilities of the child layer
            child_layer_prob = layer.probability_of_simple_event(event)  # shape: (#child_nodes, )

            # get the probabilities of the child nodes that are connected to nodes of this layer
            probabilities = child_layer_prob[edges.values()]  # shape: (#nodes, 1)

            # update result
            result[edges.indices()] *= probabilities

        return result

    @cached_property
    def support_per_node(self) -> List[Event]:
        result = [self.universal_simple_event().as_composite_set() for _ in range(self.number_of_nodes)]
        for edges, layer in zip(self.edges, self.child_layers):
            edges = edges.coalesce()
            child_layer_support = layer.support_per_node
            for index, edge in zip(edges.indices().squeeze(0), edges.values()):
                result[index] &= child_layer_support[edge]
        return result

    def log_conditional_of_simple_event(self, event: SimpleEvent) -> Tuple[Optional[Self], torch.Tensor]:

        # initialize the conditional child layers and the log probabilities
        log_probabilities = torch.zeros(self.number_of_nodes, dtype=torch.double)
        conditional_child_layers = []

        # list for collecting the remapped sparse-edge tensors per child layer
        remapped_edges = []

        # for edge bundle and child layer
        for index, (edges, child_layer) in enumerate(zip(self.edges, self.child_layers)):
            edges = edges.coalesce()

            # condition the child layer
            conditional, child_log_prob = child_layer.log_conditional_of_simple_event(event)

            # if it is entirely impossible, this layer also is
            if conditional is None:
                continue

            # update the log probabilities and child layers
            log_probabilities[edges.indices()] += child_log_prob[edges.values()]
            conditional_child_layers.append(conditional)

            # create the remapping of the node indices. nan indicates the node got deleted
            # enumerate the indices of the conditional child layer nodes
            new_node_indices = torch.arange(conditional.number_of_nodes)

            # initialize the remapping of the child layer node indices
            layer_remap = torch.full((child_layer.number_of_nodes,), torch.nan)
            layer_remap[child_log_prob > -torch.inf] = new_node_indices.float()

            # update the edges
            remapped_child_edges = layer_remap[edges.values()]
            valid_edges = ~torch.isnan(remapped_child_edges)
            new_edges = torch.sparse_coo_tensor(edges.indices()[:, valid_edges],
                                                remapped_child_edges[valid_edges].long(),
                                                (self.number_of_nodes,), is_coalesced=True)
            remapped_edges.append(new_edges)

        remapped_edges = torch.stack(remapped_edges).coalesce()

        # get nodes that should be removed as boolean mask
        remove_mask = log_probabilities.squeeze(-1) == -torch.inf  # shape (#nodes, )
        keep_mask = ~remove_mask

        # remove the nodes that have -inf log probabilities from remapped_edges
        remapped_edges = remapped_edges.index_select(1, keep_mask.nonzero().squeeze(-1))

        # construct result and clean it up
        result = self.__class__(conditional_child_layers, remapped_edges.coalesce())
        result.clean_up_orphans_inplace()
        return result, log_probabilities

    def remove_nodes_inplace(self, remove_mask: torch.BoolTensor):

        # remove nodes from the layer
        self.edges = self.edges[:, ~remove_mask]

        # remove nodes from the child layers
        for index, (edges, child_layer) in enumerate(zip(self.edges, self.child_layers)):
            # create a removal mask for the child layer
            child_layer_remove_mask = torch.ones(child_layer.number_of_nodes).bool()
            child_layer_remove_mask[edges] = False

            # remove nodes from the child layer
            child_layer.remove_nodes_inplace(child_layer_remove_mask)

            # update the edges of this layer
            self.edges[index] = shrink_index_tensor(edges.unsqueeze(-1)).squeeze(-1)

    def merge_with_one_layer_inplace(self, other: Self):
        ...

    def merge_with(self, others: List[Self]):
        raise NotImplementedError

    def clean_up_orphans_inplace(self):
        """
        Clean up the layer inplace by removing orphans in the child layers.
        """
        for index, (edges, child_layer) in enumerate(zip(self.edges, self.child_layers)):

            # mask rather nodes have parent edges or not
            orphans = torch.ones(child_layer.number_of_nodes, dtype=torch.bool)

            # mark nodes that have parents with False
            values = edges.values()
            if len(values) > 0:
                orphans[edges.values()] = False

            # if orphans exist
            if orphans.any():
                # remove them from the child layer
                child_layer.remove_nodes_inplace(orphans)

        # compress edges
        # print(self.edges)
        # shrunken_indices = shrink_index_tensor(self.edges.indices())
        # print(shrunken_indices)
        # self.edges =torch.sparse_coo_tensor(shrunken_indices, self.edges.values())

    def sample_from_frequencies(self, frequencies: torch.Tensor) -> torch.Tensor:

        # create a list of empty tensors for the samples of each variable
        concatenated_samples_per_variable = [torch.zeros(0) for _ in range(len(self.variables))]

        for index, (edges, child_layer) in enumerate(zip(self.edges, self.child_layers)):
            edges: torch.Tensor = edges.coalesce()  # shape (self.number_of_nodes,)
            squeezed_edge_indices = edges.indices().squeeze(0)

            # count the number of samples for each child node
            frequencies_for_child_layer = torch.zeros(child_layer.number_of_nodes,
                                                      dtype=torch.long)  # shape (#child_nodes)
            frequencies_for_child_layer = frequencies_for_child_layer.scatter_add(0, edges.values(),
                                                                                  frequencies[squeezed_edge_indices])

            # sample the child layer
            child_layer_samples = child_layer.sample_from_frequencies(frequencies_for_child_layer)

            # reorder the samples according to the order required by the values of the edges (request order of children)
            reordered_sample_values = child_layer_samples.index_select(0,
                                                                       edges.values().unique_consecutive()).coalesce().values()

            # write samples in the correct columns for the result
            for column in self.columns_of_child_layers[index]:
                concatenated_samples_per_variable[column] = (
                    torch.cat((concatenated_samples_per_variable[column], reordered_sample_values)))

        # assemble the result
        result_indices = create_sparse_tensor_indices_from_row_lengths(frequencies)
        result_values = torch.cat(concatenated_samples_per_variable, dim=-1)
        result = torch.sparse_coo_tensor(result_indices, result_values,
                                         size=(self.number_of_nodes, max(frequencies), len(self.variables)),
                                         is_coalesced=True)
        return result

    def cdf_of_nodes(self, events: torch.Tensor) -> torch.Tensor:
        result = torch.ones(len(events), self.number_of_nodes, dtype=torch.double)
        for columns, edges, layer in zip(self.columns_of_child_layers, self.edges, self.child_layers):
            edges = edges.coalesce()

            # calculate the cdf over the columns of the child layer
            cdf = layer.cdf_of_nodes(events[:, columns])  # shape: (#x, #child_nodes)

            # gather the cdf at the indices of the nodes that are required for the edges
            cdf = cdf[:, edges.values()]  # shape: (#x, #len(edges.values()))

            # add the gathered values to the result where the edges define the indices
            result[:, edges.indices().squeeze(0)] *= cdf

        return result

    def moment_of_nodes(self, order: torch.Tensor, center: torch.Tensor) -> torch.Tensor:
        result = torch.ones(self.number_of_nodes, len(self.variables), dtype=torch.double)
        for columns, edges, layer in zip(self.columns_of_child_layers, self.edges, self.child_layers):
            edges = edges.coalesce()

            # extract arguments for the child layer moment
            order_for_child_layer = order[columns]
            center_for_child_layer = center[columns]

            # calculate the moments over the columns of the child layer
            child_layer_moment = layer.moment_of_nodes(order_for_child_layer, center_for_child_layer)

            # gather the moments at the indices of the nodes that are required for the edges
            result[edges.indices().squeeze(0), columns] *= child_layer_moment[edges.values()].squeeze(-1)

        return result

    def __deepcopy__(self):
        child_layers = [child_layer.__deepcopy__() for child_layer in self.child_layers]
        edges = self.edges.clone()
        return self.__class__(child_layers, edges)

    def marginal(self, variables: Iterable[Variable]) -> Optional[Self]:
        if all(variable not in variables for variable in self.variables):
            return None
        marginal_child_layers = [layer.marginal(variables) for layer in self.child_layers]
        keep_mask_of_edges = torch.tensor([marginal is not None for marginal in marginal_child_layers], dtype=torch.bool)
        new_edges = self.edges.index_select(0, keep_mask_of_edges.nonzero().squeeze()).coalesce()
        return self.__class__([layer for layer in marginal_child_layers if layer is not None], new_edges)


@dataclass
class AnnotatedLayer:
    layer: Layer
    nodes: List[ProbabilisticCircuitMixin]
    hash_remap: Dict[int, int]
