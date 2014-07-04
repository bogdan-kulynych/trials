"""Useful statistics."""

from collections import OrderedDict

import numpy as np

from scipy import stats
from scipy import special as spc


SAMPLE_SIZE = 10000


def _split(variations, control=None):
    if control is None:
        control = list(variations.keys())[0]

    others = OrderedDict((label, variation) for label, variation
                         in variations.items() if label != control)
    control = variations[control]

    return control, others


def expected_posterior(variations):
    """Calculate expected posterior E[parameter | data] for each variation."""
    values = OrderedDict()
    for label, variation in variations.items():
        values[label] = variation.posterior.mean()

    return values


def posterior_credible_interval(variations, level=95):
    """Calculate posterior P(parameter | data) credible interval for each
    variation.

    Returns a 3-tuple (lower, median, upper)
    """

    values = OrderedDict()
    for label, variation in variations.items():
        left_percentile = 0.5*(100-level)/100
        left = variation.posterior.ppf(left_percentile)
        median = variation.posterior.ppf(0.5)
        right = variation.posterior.ppf((level+left_percentile)/100)
        values[label] = min(left, right), median, max(left, right)

    return values


def expected_lift(variations, control=None):
    """Calculate expected lift E[(B-A)/A]."""
    values = OrderedDict()
    control, others = _split(variations, control)
    a = control.posterior
    m = a.mean()
    for label, variation in others.items():
        b = variation.posterior
        lift = (b.mean()-m) / m
        values[label] = lift

    return values


def lift_credible_interval(variations, control=None, level=95,
                           sample_size=SAMPLE_SIZE):
    """Calculate credible interval for lift E[(B-A)/A] using MCMC.

    Returns a 3-tuple (lower, median, upper)
    """
    values = OrderedDict()
    a, others = _split(variations, control)

    for label, b in others.items():
        a_samples = a.posterior.rvs(size=sample_size)
        b_samples = b.posterior.rvs(size=sample_size)
        lift_samples = (b_samples-a_samples)/a_samples
        left_percentile = 0.5*(100-level)
        right = np.percentile(lift_samples, level+left_percentile)
        median = np.percentile(lift_samples, 50)
        left = np.percentile(lift_samples, left_percentile)
        values[label] = min(left, right), median, max(left, right)

    return values


def dominance(variations, control=None, sample_size=SAMPLE_SIZE):
    """Calculate P(A > B).

    Uses a modified Evan Miller closed formula if prior parameters are integers
    http://www.evanmiller.org/bayesian-ab-testing.html

    Uses scipy's MCMC otherwise

    TODO: The modified formula for informative prior has to be proved correct
    """
    values = OrderedDict()
    a, others = _split(variations, control)

    def is_integer(x):
        try:
            return x.is_integer()
        except:
            return int(x) == x

    for label, b in others.items():

        # If prior parameters are integers, use modified Evan Miller formula:
        if is_integer(a.prior_alpha) and is_integer(a.prior_beta) \
           and is_integer(b.prior_alpha) and is_integer(b.prior_beta):

            total = 0
            for i in range(b.alpha-b.prior_alpha):
                total += np.exp(spc.betaln(a.alpha+i, b.beta + a.beta) -
                                np.log(b.beta+i) - spc.betaln(b.prior_alpha+i,
                                b.beta) - spc.betaln(a.alpha, a.beta))
            values[label] = total

        # Use MCMC otherwise
        else:
            a_samples = a.posterior.rvs(sample_size)
            b_samples = b.posterior.rvs(sample_size)
            values[label] = np.mean(b_samples > a_samples)

    return values


def empirical_lift(variations, control=None):
    """Calculate empirical lift E[(B-A)/A]."""
    values = OrderedDict()
    a, others = _split(variations, control)
    for label, b in others.items():
        total_a = a.alpha-a.prior_alpha+a.beta-a.prior_beta
        total_b = b.alpha-b.prior_alpha+b.beta-b.prior_beta
        p_a = float(a.alpha-a.prior_alpha) / total_a
        p_b = float(b.alpha-b.prior_alpha) / total_b
        lift = (p_b - p_a) / p_a
        values[label] = lift

    return values


def ztest_dominance(variations, control=None):
    """Calculate z-test for dominance."""
    values = OrderedDict()
    a, others = _split(variations, control)
    for label, b in others.items():
        total_a = a.alpha-a.prior_alpha+a.beta-a.prior_beta
        total_b = b.alpha-b.prior_alpha+b.beta-b.prior_beta
        p_a = float(a.alpha-a.prior_alpha) / total_a
        p_b = float(b.alpha-b.prior_alpha) / total_b
        sse_a = p_a * (1-p_a) / total_a
        sse_b = p_b * (1-p_b) / total_b
        zscore = (p_b-p_a) / np.sqrt(sse_a+sse_b)
        values[label] = stats.norm().cdf(zscore)

    return values


statistic_funcs = {
    'expected posterior': expected_posterior,
    'posterior CI': posterior_credible_interval,
    'expected lift': expected_lift,
    'lift CI': lift_credible_interval,
    'empirical lift': empirical_lift,
    'dominance': dominance,
    'z-test dominance': ztest_dominance,
}
