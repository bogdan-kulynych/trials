from collections import OrderedDict

from .variants import *


class Trials(object):
    """
    Main interface for creating A/B tests.
    """

    class UnknownVtype(Exception):
        pass

    def __init__(self, variant_labels, vtype='bernoulli', *args, **kwargs):
        if isinstance(vtype, str):
            if vtype == 'bernoulli':
                vtype = BernoulliVariant
            else:
                raise Trials.UnknownVtype(vtype)

        self.vtype = vtype
        self.variants = OrderedDict([(label, vtype(*args, **kwargs)) \
            for label in variant_labels])

        self.evaluators = OrderedDict([(etype.name, etype(self)) \
            for etype in vtype.evaluator_classes])
        self.evaluation = None

    def update(self, feed):
        for label, observations in feed.items():
            self.variants[label].update(*observations)

    def evaluate(self, *args, **kwargs):
        self.evaluation = OrderedDict()
        for label, evaluator in self.evaluators.items():
            self.evaluation[label] = evaluator.evaluate(*args, **kwargs)

        return self.evaluation

    @property
    def summary(self):
        if not self.evaluation:
            self.evaluate()

        pieces = []
        for label, evaluator in self.evaluators.items():
            pieces.append('({})'.format(label))
            pieces.append(evaluator.summary)

        return '\n'.join(pieces)
