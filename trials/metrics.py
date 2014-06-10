from collections import OrderedDict

import numpy as np
from scipy import special as sp


class Lift:

    def __init__(self, variants, control=None):
        if control is None:
            control = list(variants.keys())[0]

        self.result = OrderedDict()
        control_sample = variants[control].sample()

        noncontrols = [(label, variant) for label, variant in variants.items() \
            if label != control]

        for label, variant in noncontrols:
            xs = variant.sample()
            deltas = xs - control_sample
            lift = np.mean(deltas / control_sample, axis=0)
            p = np.mean(deltas * lift > 0, axis=0)

            self.result[label] = {
                'lift': lift,
                'p': p
            }

    @property
    def best(self):
        return max(self.result, \
            key=lambda variant: self.result[variant]['lift'] * self.result[variant]['p'])

    def __str__(self):
        lines = []
        for variant, values in self.result.items():
            lines.append('{}: lift = {:.2%}, p = {:.2%}' \
                .format(variant, values['lift'], values['p']))
        return '\n'.join(lines)


class BetaDomination:
    """
    Closed formula for P(A > B) within Beta-Bernoulli model
    http://www.evanmiller.org/bayesian-ab-testing.html
    """

    def __init__(self, variants, control=None):
        if control is None:
            control = list(variants.keys())[0]

        self.result = OrderedDict()

        noncontrols = [(label, variant) for label, variant in variants.items() \
            if label != control]

        a = variants[control]

        for label, b in noncontrols:
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