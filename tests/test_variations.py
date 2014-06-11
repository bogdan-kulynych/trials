from nose import tools
import numpy as np

from trials.variations import *


class TestBernoulli:

    def setup(self):
        self.x = BernoulliVariation(1, 1)

    def test_update(self):
        self.x.update(100, 20)
        self.x.update(200, 10)
        tools.assert_true(self.x.alpha == 301)
        tools.assert_true(self.x.beta == 31)

    def test_sample(self):
        s1 = self.x.sample(10)
        tools.assert_equals(len(s1), 10)
        s2 = self.x.sample(10)
        tools.assert_true(np.all(s1 == s2))
        self.x.update(10, 30)
        s3 = self.x.sample(10)
        tools.assert_false(np.all(s2 == s3))
