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
        lift = (b.mean() - m) / m
        values[label] = lift

    return values


def domination(variations, control=None):
    """Calculates P(A > B) using a closed formula

    http://www.evanmiller.org/bayesian-ab-testing.html
    """

    values = OrderedDict()
    a, others = _split(variations, control)
    for label, b in others.items():
        total = 0
        for i in range(b.alpha - 1):
            total += np.exp(spc.betaln(a.alpha + i, b.beta + a.beta) \
                - np.log(b.beta + i) - spc.betaln(1 + i, b.beta) - \
                                        spc.betaln(a.alpha, a.beta))
        values[label] = total

    return values


def empirical_lift(variations, control=None):
    """Calculates empirical lift E[(B-A)/A]"""

    values = OrderedDict()
    a, others = _split(variations, control)
    for label, b in others.items():
        p_a = float(a.alpha-1) / (a.alpha-1 + a.beta-1)
        p_b = float(b.alpha-1) / (b.alpha-1 + b.beta-1)
        lift = (p_b - p_a) / p_a
        values[label] = lift

    return values


def frequentist_domination(variations, control=None):
    """Calculates z-test for domination"""

    values = OrderedDict()
    a, others = _split(variations, control)
    for label, b in others.items():
        p_a = float(a.alpha-1) / (a.alpha-1 + a.beta-1)
        p_b = float(b.alpha-1) / (b.alpha-1 + b.beta-1)
        sse_a = p_a * (1-p_a) / (a.alpha-1 + a.beta-1)
        sse_b = p_b * (1-p_b) / (b.alpha-1 + b.beta-1)
        z = (p_b - p_a) / np.sqrt(sse_a + sse_b)
        values[label] = stats.norm().cdf(z)

    return values


metrics = {
    'lift': lift,
    'empirical lift': empirical_lift,
    'domination': domination,
    'frequentist domination': frequentist_domination,
}