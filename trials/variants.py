import numpy as np

from collections import OrderedDict

from .evaluation import Lift
from .utils import cached


def PosteriorSampleMixin(*params):
    class PosteriorSampleMixinCls(object):

        sample_size = 5000

        @cached(*params)
        def sample(self, n=sample_size):
            return self.posterior(*[getattr(self, p) for p in params], size=n)

    return PosteriorSampleMixinCls


class BernoulliVariant(PosteriorSampleMixin('alpha', 'beta')):
    """
    Binary event variant
    """

    posterior = np.random.beta
    evaluator_classes = [Lift]

    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta

    def update(self, successes, failures):
        self.alpha += successes
        self.beta += failures


class NormalVariant(object):
    pass


class PoissonVariant(object):
    pass


class ExpVariant(object):
    pass


class LogNormalVariant(object):
    pass