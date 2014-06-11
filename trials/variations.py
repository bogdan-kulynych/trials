from scipy import stats

from collections import OrderedDict

from .metrics import metrics
from .utils import cached


class PosteriorSampleMixin(object):

    sample_size = 5000

    @cached
    def sample(self, n=sample_size):
        return self.posterior.rvs(*[getattr(self, p) for p in self.params], size=n)


class BernoulliVariation(PosteriorSampleMixin):
    """
    Bernoulli binary event variation
    """

    posterior = stats.beta
    params = ['alpha', 'beta']
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