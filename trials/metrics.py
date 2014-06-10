from collections import OrderedDict

import numpy as np
from scipy import special as sp


class Metric(object):
    def __init__(self, variants, control=None):
        if control is None:
            control = list(variants.keys())[0]

        self.control = variants[control]
        self.others = OrderedDict((label, variant) for label, variant \
            in variants.items() if label != control)


class Lift(Metric):
    """
    Calculates lifts E[(B-A)/A] and domination probabilities P(A > B) of all \
    variants relative to the control using Monte Carlo integration:
    """

    def __init__(self, variants, control=None):
        super(Lift, self).__init__(variants, control)

        self.result = OrderedDict()
        control_sample = self.control.sample()

        for label, variant in self.others.items():
            xs = variant.sample()
            deltas = xs - control_sample
            lift = np.mean(deltas / control_sample, axis=0)
            p = np.mean(deltas * lift > 0, axis=0)

            self.result[label] = {
                'lift': lift,
                'p': p
            }

    def __str__(self):
        lines = []
        for variant, values in self.result.items():
            lines.append('{}: lift = {:.2%}, p = {:.2%}' \
                .format(variant, values['lift'], values['p']))
        return '\n'.join(lines)


class BetaDomination(Metric):
    """
    Closed formula for P(A > B) within Beta-Bernoulli model
    http://www.evanmiller.org/bayesian-ab-testing.html
    """

    def __init__(self, variants, control=None):
        super(Lift, self).__init__(variants, control)

        self.result = OrderedDict()
        a = self.control
        for label, b in self.others.items():
            total = 0
            for i in range(b.alpha - 1):
                total += np.exp(sp.betaln(a.alpha + i, b.beta + a.beta) \
                    - np.log(b.beta + i) - sp.betaln(1 + i, b.beta) - sp.betaln(a.alpha, a.beta))

            self.result[label] = {
                'p': total
            }

    def __str__(self):
        lines = []
        for variant, values in self.result.items():
            lines.append('{}: p = {:.2%}' \
                .format(variant, values['p']))
        return '\n'.join(lines)


metrics = {
    'lift': Lift,
    'beta-domination': BetaDomination
}