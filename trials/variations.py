from scipy import stats

from collections import OrderedDict

from .metrics import metrics
from .utils import cached


def PosteriorSampleMixin(*params):

    class PosteriorSampleMixinCls(object):

        sample_size = 5000

        @cached(*params)
        def sample(self, n=sample_size):
            return self.posterior.rvs(*[getattr(self, p) for p in params], size=n)

    return PosteriorSampleMixinCls


class BernoulliVariation(PosteriorSampleMixin('alpha', 'beta')):
    """
    Bernoulli binary event variation
    """

    posterior = stats.beta
    metrics = ['lift', 'domination', 'z-test']

    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta

    def update(self, successes, failures):
        self.alpha += successes
        self.beta += failures


class NormalVariation(object):
    pass


class PoissonVariation(object):
    pass


class ExpVariation(object):
    pass


class LogNormalVariation(object):
    pass


vtypes = {
    'bernoulli': BernoulliVariation
}