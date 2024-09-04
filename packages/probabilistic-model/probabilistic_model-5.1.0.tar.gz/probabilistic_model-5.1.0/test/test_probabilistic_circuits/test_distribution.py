import unittest

from matplotlib import pyplot as plt
from random_events.interval import *
from random_events.variable import Integer, Continuous

from probabilistic_model.probabilistic_circuit.nx.distributions import (UniformDistribution,
                                                                        SymbolicDistribution,
                                                                        IntegerDistribution,
                                                                        GaussianDistribution)
from probabilistic_model.probabilistic_circuit.nx.probabilistic_circuit import *
from probabilistic_model.utils import MissingDict


class Animal(SetElement):
    EMPTY_SET = -1
    CAT = 0
    DOG = 1
    FISH = 2


class UniformDistributionTestCase(unittest.TestCase):
    variable = Continuous("x")
    model: UniformDistribution

    def setUp(self):
        self.model = UniformDistribution(self.variable, closed(0, 1).simple_sets[0])

    def show(self):
        nx.draw(self.model.probabilistic_circuit, with_labels=True)
        plt.show()

    def test_conditional_from_simple_event(self):
        event = SimpleEvent({self.variable: closed(0.5, 2)}).as_composite_set()
        conditional, probability = self.model.conditional(event)
        self.assertEqual(len(list(conditional.probabilistic_circuit.nodes)), 1)
        self.assertEqual(probability, 0.5)
        self.assertEqual(conditional.univariate_support, closed(0.5, 1))

    def test_conditional_from_singleton_event(self):
        event = SimpleEvent({self.variable: singleton(0.3)}).as_composite_set()
        conditional, probability = self.model.conditional(event)
        self.assertEqual(len(conditional.probabilistic_circuit.nodes), 1)
        self.assertEqual(probability, 1.)
        self.assertEqual(conditional.location, 0.3)

    def test_conditional_from_complex_event(self):
        interval = closed(0., 0.2) | closed(0.5, 1.) | singleton(0.3)
        event = SimpleEvent({self.variable: interval}).as_composite_set()
        model, likelihood = self.model.conditional(event)
        self.assertEqual(len(list(model.probabilistic_circuit.nodes)), 4)
        self.assertIsInstance(model.probabilistic_circuit.root, SumUnit)

    def test_conditional_with_none(self):
        event = SimpleEvent({self.variable: singleton(2)}).as_composite_set()
        conditional, probability = self.model.conditional(event)
        self.assertEqual(conditional, None)


class DiscreteDistributionTestCase(unittest.TestCase):
    symbol = Symbolic("animal", Animal)
    integer = Integer("x")

    symbolic_distribution: SymbolicDistribution
    integer_distribution: IntegerDistribution

    def setUp(self):
        symbolic_probabilities = MissingDict(float, {Animal.CAT: 0.1, Animal.DOG: 0.2, Animal.FISH: 0.7})
        self.symbolic_distribution = SymbolicDistribution(self.symbol, symbolic_probabilities)
        integer_probabilities = MissingDict(float, {0: 0.1, 1: 0.2, 2: 0.7})
        self.integer_distribution = IntegerDistribution(self.integer, integer_probabilities)

    def test_creation(self):
        circuit = ProbabilisticCircuit()
        circuit.add_node(self.symbolic_distribution)
        circuit.add_node(self.integer_distribution)
        self.assertEqual(len(list(circuit.nodes)), 2)

    def test_as_deterministic_sum(self):
        result = self.symbolic_distribution.as_deterministic_sum()
        self.assertEqual(len(result.subcircuits), 3)
        self.assertTrue(np.allclose(result.weights, np.array(list(self.symbolic_distribution.probabilities.values()))))
        self.assertIsInstance(result.probabilistic_circuit.root, SumUnit)


class GaussianDistributionTestCase(unittest.TestCase):
    x: Continuous = Continuous("x")
    distribution: GaussianDistribution

    def setUp(self):
        self.distribution = GaussianDistribution(self.x, 0, 1)

    def test_conditional_from_simple_interval(self):
        conditional, _ = self.distribution.conditional(SimpleEvent({self.x: closed(0, 1)}).as_composite_set())
        self.assertIsNotNone(conditional.probabilistic_circuit)
        self.assertEqual(len(list(conditional.probabilistic_circuit.nodes)), 1)
        self.assertEqual(conditional.interval, closed(0, 1).simple_sets[0])

    def test_conditional_from_complex_interval(self):
        conditional, _ = self.distribution.conditional(SimpleEvent({self.x: closed(0, 1) |
                                                                            closed(2, 3)}).as_composite_set())
        self.assertIsNotNone(conditional.probabilistic_circuit)
        self.assertEqual(len(list(conditional.probabilistic_circuit.nodes)), 3)

    def test_plot(self):
        condition = closed(-float("inf"), -1) | closed(1, float("inf"))
        distribution, _ = self.distribution.conditional(SimpleEvent({self.x: condition}).as_composite_set())
        traces = distribution.plot()
        self.assertGreater(len(traces), 0)
        # go.Figure(traces, distribution.plotly_layout()).show()


class IntegerDistributionTestCase(unittest.TestCase):
    x = Integer("x")

    model: SumUnit

    def setUp(self):
        sum_unit = SumUnit()
        i1 = IntegerDistribution(self.x, MissingDict(float, {0: 1}))
        sum_unit.add_subcircuit(i1, 0.4)
        i2 = IntegerDistribution(self.x, MissingDict(float, {1: 1}))
        sum_unit.add_subcircuit(i2, 0.6)
        self.model = sum_unit

    def test_from_sum_unit(self):
        d = IntegerDistribution.from_sum_unit(self.model)
        i = IntegerDistribution(self.x, MissingDict(float, {0: 0.4, 1: 0.6}))
        self.assertEqual(i, d)
