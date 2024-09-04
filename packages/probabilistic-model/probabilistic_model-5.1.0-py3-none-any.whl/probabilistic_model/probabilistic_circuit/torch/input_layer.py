from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import random_events
import torch
from random_events.interval import Interval, SimpleInterval, singleton
from random_events.product_algebra import Event, SimpleEvent
from random_events.sigma_algebra import AbstractCompositeSet
from random_events.variable import Continuous
from typing_extensions import List, Tuple, Self, Type

from .pc import InputLayer, AnnotatedLayer, SumLayer
from ..nx.distributions import DiracDeltaDistribution
from ...probabilistic_circuit.nx.probabilistic_circuit import ProbabilisticCircuitMixin
from .utils import remove_rows_and_cols_where_all, create_sparse_tensor_indices_from_row_lengths
from ...utils import interval_as_array


class ContinuousLayer(InputLayer, ABC):
    """
    Abstract base class for continuous univariate input units.
    """

    variable: Continuous

    @abstractmethod
    def cdf_of_nodes(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    def probability_of_simple_event(self, event: SimpleEvent) -> torch.Tensor:
        interval: Interval = event[self.variable]
        points = torch.tensor(interval_as_array(interval))
        upper_bound_cdf = self.cdf_of_nodes(points[:, (1,)])
        lower_bound_cdf = self.cdf_of_nodes(points[:, (0,)])
        return (upper_bound_cdf - lower_bound_cdf).sum(dim=0)

    def log_conditional_of_simple_event(self, event: SimpleEvent):
        if event.is_empty():
            return None, -torch.inf
        interval: Interval = event[self.variable]

        if interval.is_singleton():
            return self.log_conditional_from_singleton(interval.simple_sets[0])

        if len(interval.simple_sets) == 1:
            return self.log_conditional_from_simple_interval(interval.simple_sets[0])
        else:
            return self.log_conditional_from_interval(interval)

    def log_conditional_from_singleton(self, singleton: SimpleInterval) -> Tuple[DiracDeltaLayer, torch.Tensor]:
        """
        Calculate the conditional distribution given singleton event.

        In this case, the conditional distribution is a Dirac delta distribution and the log-likelihood is chosen
        for the log-probability.

        This method returns a Dirac delta layer that has at most the same number of nodes as the input layer.

        :param singleton: The singleton event
        :return: The dirac delta layer and the log-likelihoods with shape (something <= #singletons, 1).
        """
        value = singleton.lower
        log_likelihoods = self.log_likelihood_of_nodes(torch.tensor(value).reshape(-1, 1)).squeeze()  # shape: (#nodes, )
        possible_indices = (log_likelihoods != -torch.inf).nonzero()[0]  # shape: (#dirac-nodes, )
        filtered_likelihood = log_likelihoods[possible_indices]
        locations = torch.full_like(filtered_likelihood, value)
        layer = DiracDeltaLayer(self.variable, locations, torch.exp(filtered_likelihood))
        return layer, log_likelihoods

    @abstractmethod
    def log_conditional_from_simple_interval(self, interval: SimpleInterval) -> Tuple[Self, torch.Tensor]:
        """
        Calculate the conditional distribution given a simple interval with p(interval) > 0.
        The interval could also be a singleton.

        :param interval: The simple interval
        :return: The conditional distribution and the log-probability of the interval.
        """
        raise NotImplementedError

    def log_conditional_from_interval(self, interval: Interval) -> Tuple[SumLayer, torch.Tensor]:
        """
        Calculate the conditional distribution given an interval with p(interval) > 0.
        :param interval: The simple interval
        :return: The conditional distribution and the log-probability of the interval.
        """

        # get conditionals of each simple interval
        results = [self.log_conditional_from_simple_interval(simple_interval) for simple_interval in
                   interval.simple_sets]

        # create new input layer
        possible_layers = [layer for layer, _ in results if layer is not None]
        input_layer = possible_layers[0]
        input_layer.merge_with(possible_layers[1:])

        # stack the log probabilities
        stacked_log_probabilities = torch.stack([log_prob for _, log_prob in results])  # shape: (#simple_intervals, #nodes, 1)

        # calculate log probabilities of the entire interval
        log_probabilities = stacked_log_probabilities.logsumexp(dim=0)  # shape: (#nodes, 1)

        # remove rows and columns where all elements are -inf
        stacked_log_probabilities.squeeze_(-1)
        valid_log_probabilities = remove_rows_and_cols_where_all(stacked_log_probabilities, -torch.inf)

        # create sparse log weights
        log_weights = valid_log_probabilities.T.exp().to_sparse_coo()
        log_weights.values().log_()

        resulting_layer = SumLayer([input_layer], [log_weights])
        return resulting_layer, log_probabilities


class ContinuousLayerWithFiniteSupport(ContinuousLayer, ABC):
    """
    Abstract class for continuous univariate input units with finite support.
    """

    interval: torch.Tensor
    """
    The interval of the distribution as a tensor of shape (num_nodes, 2).
    The first column contains the lower bounds and the second column the upper bounds.
    The intervals are treated as open intervals (>/< comparator).
    """

    def __init__(self, variable, interval):
        super().__init__(variable)
        self.interval = interval

    @property
    def lower(self) -> torch.Tensor:
        return self.interval[:, 0]

    @property
    def upper(self) -> torch.Tensor:
        return self.interval[:, 1]

    @property
    def univariate_support_per_node(self) -> List[AbstractCompositeSet]:
        return [random_events.interval.open(lower.item(), upper.item()) for lower, upper in self.interval]

    def left_included_condition(self, x: torch.Tensor) -> torch.Tensor:
        """
        Check if x is included in the left bound of the intervals.
        :param x: The data
        :return: A boolean array of shape (#x, #nodes)
        """
        return self.lower < x

    def right_included_condition(self, x: torch.Tensor) -> torch.Tensor:
        """
         Check if x is included in the right bound of the intervals.
         :param x: The data
         :return: A boolean array of shape (#x, #nodes)
         """
        return x < self.upper

    def included_condition(self, x: torch.Tensor) -> torch.Tensor:
        """
         Check if x is included in the interval.
         :param x: The data
         :return: A boolean array of shape (#x, #nodes)
         """
        return self.left_included_condition(x) & self.right_included_condition(x)

    def remove_nodes_inplace(self, remove_mask: torch.BoolTensor):
        self.interval = self.interval[~remove_mask]


class DiracDeltaLayer(ContinuousLayer):

    location: torch.Tensor
    """
    The locations of the Dirac delta distributions.
    """

    density_cap: torch.Tensor
    """
    The density caps of the Dirac delta distributions.
    This value will be used to replace infinity in likelihoods.
    """

    def __init__(self, variable: Continuous, location: torch.Tensor, density_cap: Optional[torch.Tensor] = None):
        super().__init__(variable)
        self.location = location
        self.density_cap = density_cap if density_cap is not None else torch.full_like(location, torch.inf)

    def validate(self):
        assert self.location.shape == self.density_cap.shape, "The shapes of the location and density cap must match."
        assert all(self.density_cap > 0), "The density cap must be positive."

    @property
    def number_of_nodes(self) -> int:
        return len(self.location)

    def log_likelihood_of_nodes(self, x: torch.Tensor) -> torch.Tensor:
        return torch.where(x == self.location, torch.log(self.density_cap), -torch.inf)

    @classmethod
    def original_class(cls) -> Tuple[Type, ...]:
        return DiracDeltaDistribution,

    @classmethod
    def create_layer_from_nodes_with_same_type_and_scope(cls, nodes: List[ProbabilisticCircuitMixin],
                                                         child_layers: List[AnnotatedLayer]) -> \
            AnnotatedLayer:
        hash_remap = {hash(node): index for index, node in enumerate(nodes)}
        locations = torch.tensor([node.location for node in nodes], dtype=torch.double)
        density_caps = torch.tensor([node.density_cap for node in nodes], dtype=torch.double)
        result = cls(nodes[0].variable, locations, density_caps)
        return AnnotatedLayer(result, nodes, hash_remap)

    @property
    def univariate_support_per_node(self) -> List[AbstractCompositeSet]:
        return [singleton(location.item()) for location in self.location]

    def log_mode_of_nodes(self) -> Tuple[List[Event], torch.Tensor]:
        return self.support_per_node, self.density_cap.log()

    def log_conditional_from_simple_interval(self, interval: SimpleInterval) -> Tuple[Self, torch.Tensor]:
        probabilities = self.probability_of_simple_event(SimpleEvent({self.variable: interval})).log()

        valid_probabilities = probabilities > -torch.inf

        if not valid_probabilities.any():
            return self.impossible_condition_result

        result = self.__class__(self.variable, self.location[valid_probabilities],
                                self.density_cap[valid_probabilities])
        return result, probabilities

    def merge_with(self, others: List[Self]):
        self.location = torch.cat([self.location] + [other.location for other in others])
        self.density_cap = torch.cat([self.density_cap] + [other.density_cap for other in others])

    def cdf_of_nodes(self, x: torch.Tensor) -> torch.Tensor:
        return torch.where(x < self.location, 0, 1).double()

    def remove_nodes_inplace(self, remove_mask: torch.BoolTensor):
        self.location = self.location[~remove_mask]
        self.density_cap = self.density_cap[~remove_mask]

    def sample_from_frequencies(self, frequencies: torch.Tensor) -> torch.Tensor:
        max_frequency = max(frequencies)
        result_indices = create_sparse_tensor_indices_from_row_lengths(frequencies)
        values = self.location.repeat_interleave(frequencies).unsqueeze(-1)
        result = torch.sparse_coo_tensor(result_indices, values, (self.number_of_nodes, max_frequency, 1),
                                         is_coalesced=True)
        return result

    def moment_of_nodes(self, order: torch.Tensor, center: torch.Tensor) -> torch.Tensor:
        order = order.item()
        center = center.item()
        if order == 0:
            result = torch.ones(self.number_of_nodes)
        if order == 1:
            result = self.location - center
        else:
            result = torch.zeros(self.number_of_nodes)
        return result.unsqueeze(-1)

    def __deepcopy__(self):
        return self.__class__(self.variable, self.location.clone(), self.density_cap.clone())
