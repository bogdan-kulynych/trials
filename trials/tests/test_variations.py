from nose import tools

from trials.variations import *


class TestBernoulli:

    def setup(self):
        self.var = BernoulliVariation(1, 1)

    def test_update(self):
        self.var.update(100, 20)
        self.var.update(200, 10)
        tools.assert_true(self.var.alpha == 301)
        tools.assert_true(self.var.beta == 31)

    def test_posterior(self):
        self.var.update(150, 50)

        m = self.var.posterior.mean()
        self.var.posterior.var()
        tools.assert_true(0.7 < m < 0.9)
