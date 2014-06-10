from collections import OrderedDict

import numpy as np


class Lift(object):

    name = 'lift'

    def __init__(self, processor):
        self.processor = processor
        self.evaluation = None

    def evaluate(self, control=None):
        variants = self.processor.variants

        if control is None:
            control = list(variants.keys())[0]

        self.evaluation = OrderedDict()
        control_sample = variants[control].sample()

        noncontrols = [(label, variant) for label, variant in variants.items() \
            if label != control]

        for label, variant in noncontrols:
            xs = variant.sample()
            deltas = xs - control_sample
            lift = np.mean(deltas / control_sample, axis=0)
            p = np.mean(deltas * lift > 0, axis=0)

            self.evaluation[label] = {
                'lift': lift,
                'p': p
            }

        return self.evaluation

    @property
    def summary(self):
        if not self.evaluation:
            self.evaluate()

        lines = []
        for variant, metrics in self.evaluation.items():
            lines.append('{}: lift = {:.2%}, p = {:.2%}' \
                .format(variant, metrics['lift'], metrics['p']))
        return '\n'.join(lines)


