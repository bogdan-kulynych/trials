from scipy import stats

from collections import OrderedDict

from .metrics import metrics
from .utils import cached


class Variation(object):

    @property
    def rv(self):
        """
        Returns posterior as a frozen Random Variable
        """
        return self.posterior(*[getattr(self, param) for param in self.params])


class BernoulliVariation(Variation):
    """
    Bernoulli binary event variation
    """

    posterior = stats.beta
    params = ['alpha', 'beta']
    metrics = ['lift', 'empirical lift', 'domination', 'frequentist domination']

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