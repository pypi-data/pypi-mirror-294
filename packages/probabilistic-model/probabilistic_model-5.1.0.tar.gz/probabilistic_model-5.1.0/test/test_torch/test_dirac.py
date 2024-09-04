import math
import unittest

import torch
from random_events.interval import closed, singleton
from random_events.product_algebra import SimpleEvent
from random_events.variable import Continuous
from torch.testing import assert_close

from probabilistic_model.probabilistic_circuit.torch.input_layer import DiracDeltaLayer


class DiracDeltaLayerTestCase(unittest.TestCase):

    x: Continuous = Continuous("x")
    p_x = DiracDeltaLayer(x, torch.tensor([0., 1.]).double(), torch.tensor([1., 2.]).double())

    def test_likelihood(self):
        data = torch.tensor([0, 1, 2]).reshape(-1, 1)
        ll = self.p_x.log_likelihood_of_nodes(data)
        self.assertEqual(ll.shape, torch.Size((len(data), self.p_x.number_of_nodes)))
        result = [[0, -torch.inf],
                  [-torch.inf, math.log(2)],
                  [-torch.inf, -torch.inf]]
        assert_close(ll, torch.tensor(result).double())

    def test_support_per_node(self):
        support = self.p_x.support_per_node
        result = [SimpleEvent({self.x: singleton(0)}).as_composite_set(),
                  SimpleEvent({self.x: singleton(1)}).as_composite_set()]
        self.assertEqual(support, result)

    def test_conditional_of_simple_interval(self):
        interval = closed(-0.5, 0.5).simple_sets[0]
        layer, ll = self.p_x.log_conditional_from_simple_interval(interval)
        result = torch.tensor([1, 0]).log().double()
        assert_close(ll, result)
        layer.validate()
        self.assertEqual(layer.number_of_nodes, 1)
        assert_close(layer.location, torch.tensor([0.]).double())
        assert_close(layer.density_cap, torch.tensor([1.]).double())

    def test_sample(self):
        s = self.p_x.sample_from_frequencies(torch.tensor([10, 5]))
        self.assertEqual(s.values().shape, torch.Size((15, 1)))
        self.assertTrue(torch.all(s.values()[:10] == 0.))
        self.assertTrue(torch.all(s.values()[10:] == 1.))

    def test_cdf(self):
        data = torch.tensor([-1, 0, 1, 2]).unsqueeze(-1).double()
        cdf = self.p_x.cdf_of_nodes(data)
        result = torch.tensor([[0, 0], [1, 0], [1, 1], [1, 1]]).double()
        assert_close(cdf, result)

    def test_moment(self):
        order = torch.tensor([1.]).long()
        center = torch.tensor([1.5]).double()
        moment = self.p_x.moment_of_nodes(order, center)
        result = torch.tensor([-1.5, -0.5]).double().unsqueeze(-1)
        assert_close(moment, result)

    def test_mode(self):
        mode, ll = self.p_x.log_mode_of_nodes()
        result_ll = torch.tensor([1, 2]).log().double()
        assert_close(result_ll, ll)
        self.assertEqual(mode, self.p_x.support_per_node)


if __name__ == '__main__':
    unittest.main()
