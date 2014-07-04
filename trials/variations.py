"""Variations class."""

from scipy import stats


class BernoulliVariation(object):

    """Variation that assumes binary Bernoulli events."""

    stats = ['expected posterior', 'posterior CI',
             'expected lift', 'lift CI', 'empirical lift',
             'dominance', 'z-test dominance']

    # By default uses Jeffreys' prior
    # Call with alpha=1, beta=1 to use flat prior
    def __init__(self, alpha=0.5, beta=0.5):
        """Create a variation."""
        self.prior_alpha = alpha
        self.prior_beta = beta

        self.alpha = alpha
        self.beta = beta

    def update(self, successes, failures):
        """Update variation state with observations."""
        self.alpha += successes
        self.beta += failures

    @property
    def posterior(self):
        """Return posterior as scipy frozen random variable."""
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
