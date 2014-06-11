from collections import OrderedDict

import numpy as np

from scipy import stats
from scipy import special as spc


class MetricResult(object):

    def __init__(self, title, values):
        self.title = title
        self.values = values

    def __str__(self):
        lines = []
        for variation, value in self.values.items():
            lines.append('{}: {} = {:.2%}' \
                .format(variation, self.title, value))
        return '\n'.join(lines)


def split(variations, control=None):
    if control is None:
        control = list(variations.keys())[0]

    others = OrderedDict((label, variation) for label, variation \
        in variations.items() if label != control)
    control = variations[control]

    return control, others


def lift(variations, control=None):
    """
    Calculates expected lift E[(B-A)/A]
    """
    values = OrderedDict()
    control, others = split(variations, control)
    for label, variation in others.items():
        a = stats.beta(control.alpha, control.beta)
        b = stats.beta(variation.alpha, variation.beta)
        m = a.mean()
        lift = (b.mean() - m) / m
        values[label] = lift

    return MetricResult('lift', values)


def domination(variations, control=None):
    """
    Calculates P(A > B) using a closed formula
    http://www.evanmiller.org/bayesian-ab-testing.html
    """
    values = OrderedDict()
    a, others = split(variations, control)
    for label, b in others.items():
        total = 0
        for i in range(b.alpha - 1):
            total += np.exp(spc.betaln(a.alpha + i, b.beta + a.beta) \
                - np.log(b.beta + i) - spc.betaln(1 + i, b.beta) - \
                                        spc.betaln(a.alpha, a.beta))
        values[label] = total

    return MetricResult('p', values)


def ztest(variations, control=None):
    """
    Calculates z-test p-value for normal distribution
    """
    values = OrderedDict()
    a, others = split(variations, control)
    for label, b in others.items():
        p_a = float(a.alpha-1) / (a.alpha-1 + a.beta-1)
        p_b = float(b.alpha-1) / (b.alpha-1 + b.beta-1)
        sse_a = p_a * (1-p_a) / (a.alpha-1 + a.beta-1)
        sse_b = p_b * (1-p_b) / (b.alpha-1 + b.beta-1)
        z = (p_b - p_a) / np.sqrt(sse_a + sse_b)
        values[label] = stats.norm().cdf(z)
    return MetricResult('p', values)


metrics = {
    'lift': lift,
    'domination': domination,
    'z-test': ztest
}