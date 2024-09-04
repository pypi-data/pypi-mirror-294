import json
import math
import tempfile
import unittest
from datetime import datetime

import networkx as nx
import numpy as np
import pandas as pd
import random_events
import sklearn.datasets
from jpt import infer_from_dataframe as old_infer_from_dataframe
from jpt.learning.impurity import Impurity
from jpt.trees import JPT as OldJPT
from matplotlib import pyplot as plt
from random_events.interval import closed, singleton
from random_events.product_algebra import SimpleEvent
from random_events.set import SetElement
from random_events.variable import Variable
from sortedcontainers import SortedSet

from probabilistic_model.bayesian_network.bayesian_network import BayesianNetwork
from probabilistic_model.bayesian_network.distributions import (RootDistribution, ConditionalProbabilisticCircuit,
                                                                ConditionalProbabilityTable)
from probabilistic_model.distributions.multinomial import MultinomialDistribution
from probabilistic_model.learning.jpt.jpt import JPT
from probabilistic_model.learning.jpt.variables import (ScaledContinuous, infer_variables_from_dataframe, Integer,
                                                        Symbolic, Continuous)
from probabilistic_model.learning.nyga_distribution import NygaDistribution
from probabilistic_model.probabilistic_circuit.nx.distributions import IntegerDistribution, \
    SymbolicDistribution
from probabilistic_model.probabilistic_circuit.nx.probabilistic_circuit import ProductUnit, \
    SumUnit, ProbabilisticCircuit
from probabilistic_model.utils import MissingDict


class ShowMixin:
    model: JPT

    def show(self):
        nx.draw(self.model.probabilistic_circuit, with_labels=True)
        plt.show()


class VariableTestCase(unittest.TestCase):
    variable: ScaledContinuous = ScaledContinuous('x', 2, 3)

    def test_encode(self):
        self.assertEqual(self.variable.encode(2), 0)
        self.assertEqual(self.variable.encode(5), 1)
        self.assertEqual(self.variable.encode(0), -2 / 3)

    def test_decode(self):
        self.assertEqual(self.variable.decode(0), 2)
        self.assertEqual(self.variable.decode(1), 5)
        self.assertEqual(self.variable.decode(-2 / 3), 0)

    def test_serialization_integer(self):
        variable = Integer('x', 2, 1)
        serialized = variable.to_json()
        deserialized = Variable.from_json(serialized)
        self.assertEqual(variable, deserialized)

    def test_serialization_continuous(self):
        variable = ScaledContinuous('x', 2, 3, 1., 0.1, 10)
        serialized = variable.to_json()
        deserialized = Variable.from_json(serialized)
        self.assertEqual(variable, deserialized)


class SymbolEnum(SetElement):
    """
    A simple enum for testing purposes.
    """
    EMPTY_SET = -1
    A = 0
    B = 1
    C = 2


class InferFromDataFrameTestCase(unittest.TestCase):
    data: pd.DataFrame

    @classmethod
    def setUpClass(cls):
        np.random.seed(69)
        data = pd.DataFrame()
        data["real"] = np.random.normal(2, 4, 100)
        data["integer"] = np.concatenate((np.random.randint(low=0, high=4, size=50), np.random.randint(7, 10, 50)))
        data["symbol"] = np.random.randint(0, 4, 100).astype(str)
        cls.data = data

    def test_types(self):
        self.assertEqual(self.data.dtypes.iloc[0], float)
        self.assertEqual(self.data.dtypes.iloc[1], int)
        self.assertEqual(self.data.dtypes.iloc[2], object)

    def test_infer_from_dataframe_with_scaling(self):
        real, integer, symbol = infer_variables_from_dataframe(self.data, scale_continuous_types=True)
        self.assertEqual(real.name, "real")
        self.assertIsInstance(real, ScaledContinuous)
        self.assertEqual(integer.name, "integer")
        self.assertEqual(symbol.name, "symbol")
        self.assertLess(real.minimal_distance, 1.)

    def test_infer_from_dataframe_without_scaling(self):
        real, integer, symbol = infer_variables_from_dataframe(self.data, scale_continuous_types=False)
        self.assertNotIsInstance(real, ScaledContinuous)

    def test_unknown_type(self):
        df = pd.DataFrame()
        df["time"] = [datetime.now()]
        with self.assertRaises(ValueError):
            infer_variables_from_dataframe(df)


class JPTTestCase(unittest.TestCase):
    data: pd.DataFrame
    real: ScaledContinuous
    integer: Integer
    symbol: Symbolic
    model: JPT

    def setUp(self):
        np.random.seed(69)
        data = pd.DataFrame()
        data["integer"] = np.concatenate((np.random.randint(low=0, high=4, size=50), np.random.randint(7, 10, 50)))
        data["real"] = np.random.normal(2, 4, 100)
        data["symbol"] = np.random.randint(0, 4, 100).astype(str)
        self.data = data
        self.real, self.integer, self.symbol = infer_variables_from_dataframe(self.data, scale_continuous_types=False)
        self.model = JPT([self.real, self.integer, self.symbol])

    def test_construct_impurity(self):
        impurity = self.model.construct_impurity()
        self.assertIsInstance(impurity, Impurity)

    def test_create_leaf_node(self):
        preprocessed_data = self.model.preprocess_data(self.data)
        leaf_node = self.model.create_leaf_node(preprocessed_data)

        self.assertEqual(len(leaf_node.subcircuits), 3)
        self.assertIsInstance(leaf_node.subcircuits[0], IntegerDistribution)
        self.assertIsInstance(leaf_node.subcircuits[1], NygaDistribution)
        self.assertIsInstance(leaf_node.subcircuits[2], SymbolicDistribution)

        # check that all likelihoods are greater than 0
        likelihood = leaf_node.likelihood(preprocessed_data)
        self.assertTrue(all(likelihood > 0))

    def test_fit_without_sum_units(self):
        self.model.min_impurity_improvement = 1
        self.model.fit(self.data)
        self.assertEqual(len(self.model.subcircuits), 1)
        self.assertEqual(self.model.weighted_subcircuits[0][0], 1.)
        self.assertEqual(len(self.model.subcircuits[0].subcircuits), 3)

    def test_fit(self):
        self.model._min_samples_leaf = 10
        self.model.fit(self.data)
        self.assertTrue(len(self.model.subcircuits) <= math.floor(len(self.data) / self.model.min_samples_leaf))
        self.assertTrue(all([weight > 0 for weight, _ in self.model.weighted_subcircuits]))

        # check that all likelihoods are greater than 0
        preprocessed_data = self.model.preprocess_data(self.data)
        likelihood = self.model.likelihood(preprocessed_data)

        self.assertTrue(all(likelihood > 0))

    def test_preprocessing_and_compare_to_jpt(self):
        variables = old_infer_from_dataframe(self.data, scale_numeric_types=False, precision=0.)
        original_jpt = OldJPT(variables, min_samples_leaf=self.model.min_samples_leaf,
                              min_impurity_improvement=self.model.min_impurity_improvement)
        original_preprocessing = original_jpt._preprocess_data(self.data)
        own_preprocessing = self.model.preprocess_data(self.data)

        # Symbolic columns are not preprocessed in order in JPTs. The difference is intended
        self.assertTrue(np.all(original_preprocessing[:, :-1] == own_preprocessing[:, :-1]))

    def test_fit_and_compare_to_jpt(self):
        self.model._min_samples_leaf = 10
        self.model.keep_sample_indices = True
        self.model.fit(self.data)
        variables = old_infer_from_dataframe(self.data, scale_numeric_types=False, precision=0.)
        original_jpt = OldJPT(variables, min_samples_leaf=self.model.min_samples_leaf,
                              min_impurity_improvement=self.model.min_impurity_improvement)
        original_jpt = original_jpt.learn(self.data, keep_samples=True)
        self.assertEqual(len(self.model.subcircuits), len(original_jpt.leaves))

        for original_leaf, new_leaf in zip(original_jpt.leaves.values(), self.model.subcircuits):
            self.assertSetEqual(set(original_leaf.s_indices), set(new_leaf.sample_indices))

    def test_jpt_continuous_variables_only(self):
        data = self.data[["real"]]
        variables = infer_variables_from_dataframe(data)
        model = JPT(variables)
        model.fit(data)
        self.assertEqual(len(model.subcircuits), 1)

    def test_jpt_integer_variables_only(self):
        data = self.data[["integer"]]
        variables = infer_variables_from_dataframe(data)
        model = JPT(variables)
        model.fit(data)
        self.assertEqual(len(model.subcircuits), 1)

    def test_jpt_symbolic_variables_only(self):
        data = self.data[["symbol"]]
        variables = infer_variables_from_dataframe(data)
        model = JPT(variables)
        model.fit(data)
        self.assertEqual(len(model.subcircuits), 4)

    def test_plot(self):
        self.model._min_samples_leaf = 10
        self.model.fit(self.data)
        fig = self.model.plot()
        self.assertIsNotNone(fig)
        # fig.show()

    def test_variable_dependencies_to_json(self):
        serialized = self.model._variable_dependencies_to_json()
        all_variable_names = [variable.name for variable in self.model.variables_from_init]
        self.assertEqual(serialized,
                         {'real': all_variable_names, 'integer': all_variable_names, 'symbol': all_variable_names})

    def test_serialization(self):
        self.model._min_samples_leaf = 10
        self.model.fit(self.data)
        serialized = self.model.to_json()
        deserialized = JPT.from_json(serialized)
        self.assertEqual(self.model, deserialized)


class BreastCancerTestCase(unittest.TestCase, ShowMixin):
    data: pd.DataFrame
    model: JPT

    @classmethod
    def setUpClass(cls):
        data = sklearn.datasets.load_breast_cancer(as_frame=True)

        df = data.data
        target = data.target.astype(str)
        target[target == "1"] = "malignant"
        target[target == "0"] = "friendly"

        df["malignant"] = target
        cls.data = df

        variables = infer_variables_from_dataframe(cls.data, scale_continuous_types=False)

        cls.model = JPT(variables, min_samples_leaf=0.4)
        cls.model.fit(cls.data)

    def test_serialization(self):
        json_dict = self.model.to_json()
        model = JPT.from_json(json_dict)

        self.assertEqual(model, self.model)

        file = tempfile.NamedTemporaryFile()

        with open(file.name, "w") as f:
            json.dump(json_dict, f)

        with open(file.name, "r") as f:
            model_ = json.load(f)
        model_ = JPT.from_json(model_)

        self.assertEqual(model, model_)
        file.close()

    def test_conditional_inference(self):
        evidence = SimpleEvent({variable: variable.domain for variable in self.model.variables}).as_composite_set()
        query = evidence
        conditional_model, evidence_probability = self.model.conditional(evidence)
        self.assertAlmostEqual(1., evidence_probability)
        self.assertAlmostEqual(1., conditional_model.probability(query))

    def test_univariate_continuous_marginal(self):
        marginal = self.model.marginal(self.model.variables[:1])
        self.assertIsInstance(marginal, NygaDistribution)

    def test_univariate_symbolic_marginal(self):
        variables = [v for v in self.model.variables if v.name == "malignant"]
        marginal = self.model.marginal(variables)
        self.assertIsInstance(marginal, SymbolicDistribution)

    def test_univariate_symbolic_marginal_as_sum_unit(self):
        variables = [v for v in self.model.variables if v.name == "malignant"]
        marginal = self.model.marginal(variables, as_deterministic_sum=True)
        self.assertIsInstance(marginal, SumUnit)

    def test_serialization_of_circuit(self):
        json_dict = self.model.probabilistic_circuit.to_json()
        model = ProbabilisticCircuit.from_json(json_dict)
        event = SimpleEvent({variable: variable.domain for variable in self.model.variables}).as_composite_set()
        self.assertAlmostEqual(model.probability(event), 1.)

    def test_marginal_conditional_chain(self):
        model = self.model.probabilistic_circuit
        marginal = model.marginal(self.model.variables[:2])
        x, y = self.model.variables[:2]
        conditional, probability = model.conditional(SimpleEvent({x: closed(0, 10)}).as_composite_set())

    def test_mode(self):
        mode, likelihood = self.model.mode()
        self.assertGreater(len(mode.simple_sets), 0)


class MNISTTestCase(unittest.TestCase):
    model: JPT

    @classmethod
    def setUpClass(cls):
        mnist = sklearn.datasets.load_digits(as_frame=True)
        df = mnist.data
        target = mnist.target
        df["digit"] = target
        df["digit"] = df['digit'].astype(str)

        variables = infer_variables_from_dataframe(df, scale_continuous_types=False, min_likelihood_improvement=0.01)
        cls.model = JPT(variables, min_samples_leaf=0.1)
        cls.model.fit(df)

    def test_serialization(self):
        json_dict = self.model.to_json()
        model = JPT.from_json(json_dict)
        self.assertEqual(model, self.model)

        file = tempfile.NamedTemporaryFile()

        with open(file.name, "w") as f:
            json.dump(json_dict, f)

        with open(file.name, "r") as f:
            model_ = json.load(f)
        model_ = JPT.from_json(model_)
        self.assertEqual(model, model_)
        file.close()


class BayesianJPTTestCase(unittest.TestCase):
    model_sl_sw: JPT
    model_pl_pw: JPT
    model_species: JPT

    sl: Continuous
    sw: Continuous
    pl: Continuous
    pw: Continuous
    species: Integer

    species_sepal_interaction_term: MultinomialDistribution
    species_petal_interaction_term: MultinomialDistribution

    subcircuit_indices: pd.DataFrame

    species_latent_variable: random_events.variable.Symbolic
    sepal_latent_variable: random_events.variable.Symbolic
    petal_latent_variable: random_events.variable.Symbolic

    @classmethod
    def setUpClass(cls):
        iris = sklearn.datasets.load_iris(as_frame=True)
        df = iris.data
        target = iris.target
        df["species"] = target

        variables = infer_variables_from_dataframe(df, scale_continuous_types=False, min_likelihood_improvement=0.1)

        cls.sl, cls.sw, cls.pl, cls.pw, cls.species = variables

        model_sl_sw = JPT(variables, min_samples_leaf=0.4, features=[cls.sl, cls.sw], targets=variables)
        model_sl_sw.fit(df)

        cls.model_sl_sw = model_sl_sw.marginal([cls.sl, cls.sw])

        model_pl_pw = JPT(variables, min_samples_leaf=0.4, features=[cls.pl, cls.pw], targets=variables)
        model_pl_pw.fit(df)
        cls.model_pl_pw = model_pl_pw.marginal([cls.pl, cls.pw])

        model_species = JPT(variables, min_samples_leaf=0.3, features=[cls.species], targets=variables)
        model_species.fit(df)
        cls.model_species = model_species.marginal([cls.species], simplify_if_univariate=False)

        subcircuit_indices = np.zeros((len(df), 3))
        subcircuit_indices[:, 0] = cls.model_sl_sw.sub_circuit_index_of_samples(df[["sepal length (cm)",
                                                                                    "sepal width (cm)"]].values)
        subcircuit_indices[:, 1] = cls.model_pl_pw.sub_circuit_index_of_samples(df[["petal length (cm)",
                                                                                    "petal width (cm)"]].values)
        subcircuit_indices[:, 2] = cls.model_species.sub_circuit_index_of_samples(df[["species"]].values)

        cls.subcircuit_indices = pd.DataFrame(subcircuit_indices, columns=["sl_sw", "pl_pw", "species"])

        cls.species_latent_variable = cls.model_species.latent_variable
        cls.sepal_latent_variable = cls.model_sl_sw.latent_variable
        cls.petal_latent_variable = cls.model_pl_pw.latent_variable

        cls.species_sepal_interaction_term = MultinomialDistribution(
            [cls.sepal_latent_variable, cls.species_latent_variable])
        cls.species_sepal_interaction_term.fit(subcircuit_indices[:, (0, 2)])

        cls.species_petal_interaction_term = MultinomialDistribution(
            [cls.petal_latent_variable, cls.species_latent_variable])
        cls.species_petal_interaction_term.fit(subcircuit_indices[:, (1, 2)])

    def test_setup(self):
        self.assertEqual(self.model_sl_sw.variables, SortedSet([self.sl, self.sw]))
        self.assertEqual(self.model_pl_pw.variables, SortedSet([self.pl, self.pw]))
        self.assertEqual(self.model_species.variables, SortedSet([self.species]))

        self.assertGreater(len(self.model_sl_sw.subcircuits), 1)
        self.assertGreater(len(self.model_pl_pw.subcircuits), 1)
        self.assertGreater(len(self.model_species.subcircuits), 1)

        self.assertFalse(self.subcircuit_indices.isna().any().any())

        self.assertEqual(self.species_petal_interaction_term.probabilities.sum(), 1.)
        self.assertEqual(self.species_sepal_interaction_term.probabilities.sum(), 1.)

    def test_to_bayesian_network(self):
        # create bayesian network with root node
        bayesian_network = BayesianNetwork()
        root = RootDistribution(self.species_latent_variable, MissingDict(float, zip([0, 1, 2],
                                                                                     self.model_species.weights)))
        self.assertEqual(list(root.probabilities.values()), [1 / 3] * 3)
        bayesian_network.add_node(root)

        p_species = ConditionalProbabilisticCircuit(self.model_species.variables)
        p_species.from_unit(self.model_species)
        bayesian_network.add_node(p_species)
        bayesian_network.add_edge(root, p_species)

        # mount the interaction term with the latent variable of the sepal distribution
        p_sepal_species = ConditionalProbabilityTable(self.sepal_latent_variable)
        p_sepal_species.from_multinomial_distribution(self.species_sepal_interaction_term)
        bayesian_network.add_node(p_sepal_species)
        bayesian_network.add_edge(root, p_sepal_species)

        # mount the distributions of the sepal variables
        p_sepal = ConditionalProbabilisticCircuit(self.model_sl_sw.variables)
        p_sepal.from_unit(self.model_sl_sw)
        [self.assertIsInstance(circuit.root, ProductUnit) for circuit in
         p_sepal.conditional_probability_distributions.values()]
        bayesian_network.add_node(p_sepal)
        bayesian_network.add_edge(p_sepal_species, p_sepal)

        # mount the interaction term with the latent variable of the petal distribution
        p_petal_species = ConditionalProbabilityTable(self.petal_latent_variable)
        p_petal_species.from_multinomial_distribution(self.species_petal_interaction_term)
        bayesian_network.add_node(p_petal_species)
        bayesian_network.add_edge(root, p_petal_species)

        # mount the distributions of the petal variables
        p_petal = ConditionalProbabilisticCircuit(self.model_pl_pw.variables)
        p_petal.from_unit(self.model_pl_pw)
        [self.assertIsInstance(circuit.root, ProductUnit) for circuit in
         p_petal.conditional_probability_distributions.values()]
        bayesian_network.add_node(p_petal)
        bayesian_network.add_edge(p_petal_species, p_petal)

        # test some queries
        bn_as_circuit = bayesian_network.as_probabilistic_circuit()
        self.assertAlmostEqual(bn_as_circuit.probability(bn_as_circuit.universal_simple_event().as_composite_set()), 1)

        e_species_1 = SimpleEvent({self.species: singleton(0)}).as_composite_set()
        #  bn_p_species_1 = bayesian_network.probability(e_species_1)
        # self.assertAlmostEqual(bn_p_species_1, 1 / 3)
        self.assertAlmostEqual(bayesian_network.as_probabilistic_circuit().probability(e_species_1), 1 / 3)

        complex_event = SimpleEvent(
            {self.species: singleton(0), self.sl: closed(4.5, 5.5)}).as_composite_set()
        pc = bayesian_network.as_probabilistic_circuit()
        pc_m = pc.marginal([v for v in pc.variables if not v.name.endswith(".latent")]).simplify()
        self.assertEqual(pc_m.variables, SortedSet([self.pl, self.pw, self.sl, self.sw, self.species]))

        self.assertAlmostEqual(pc_m.probability(complex_event), 0.2333333)
        self.assertLess(len(pc_m.weighted_edges), 3 * math.prod([len(v.domain.simple_sets) for v in bayesian_network.variables]))
