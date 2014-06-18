from collections import OrderedDict

import numpy as np

from scipy import stats
from scipy import special as spc


def _split(variations, control=None):
    if control is None:
        control = list(variations.keys())[0]

    others = OrderedDict((label, variation) for label, variation \
        in variations.items() if label != control)
    control = variations[control]

    return control, others


def lift(variations, control=None):
    """Calculates expected lift E[(B-A)/A]"""

    values = OrderedDict()
    control, others = _split(variations, control)
    a = control.rv
    m = a.mean()
    for label, variation in others.items():
        b = variation.rv
        lift = (b.mean()-m) / m
        values[label] = lift

    return values


def dominance(variations, control=None, sample_size=10000):
    """Calculates P(A > B)

    Uses a modified Evan Miller closed formula if prior parameters are integers
    http://www.evanmiller.org/bayesian-ab-testing.html

    Uses scipy's MCMC otherwise

    TODO: The modified formula for informative prior has to proved correct
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
                total += np.exp(spc.betaln(a.alpha+i, b.beta + a.beta) \
                    - np.log(b.beta+i) - spc.betaln(b.prior_alpha+i, b.beta) -\
                                            spc.betaln(a.alpha, a.beta))
            values[label] = total

        # Use MCMC otherwise
        else:
            a_samples = a.rv.rvs(sample_size)
            b_samples = b.rv.rvs(sample_size)
            values[label] = np.mean(b_samples > a_samples)

    return values


def empirical_lift(variations, control=None):
    """Calculates empirical lift E[(B-A)/A]"""

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
    """Calculates z-test for dominance"""

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


metrics = {
    'lift': lift,
    'empirical lift': empirical_lift,
    'dominance': dominance,
    'z-test dominance': ztest_dominance,
}