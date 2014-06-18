from scipy import stats

from collections import OrderedDict

from .metrics import metrics


class BernoulliVariation(object):
    """Variation that assumes binary Bernoulli events"""

    metrics = ['expected lift', 'lift CI', 'empirical lift', \
        'dominance', 'z-test dominance']

    # By default uses informative Jeffreys' prior
    # Call with alpha=1, beta=1 to use uninformative prior
    def __init__(self, alpha=0.5, beta=0.5):
        self.prior_alpha = alpha
        self.prior_beta = beta

        self.alpha = alpha
        self.beta = beta

    def update(self, successes, failures):
        self.alpha += successes
        self.beta += failures

    @property
    def posterior(self):
        return stats.beta(self.alpha, self.beta)


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