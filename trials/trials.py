from collections import OrderedDict

from .variants import vtypes as default_vtypes
from .metrics import metrics as default_metrics


class Trials(object):
    """
    Main interface for creating A/B tests.
    """

    class UnknownVariantType(Exception):
        pass

    def __init__(self, variant_labels, vtype='bernoulli', *args, **kwargs):
        if isinstance(vtype, str):
            vtype = default_vtypes[vtype]

        self.vtype = vtype
        self.variants = OrderedDict([(label, vtype(*args, **kwargs)) \
            for label in variant_labels])

    def update(self, feed):
        for label, observations in feed.items():
            self.variants[label].update(*observations)

    def evaluate(self, metric='lift', *args, **kwargs):
        result = None
        if isinstance(metric, str):
            cls = default_metrics[metric]
            result = cls(self.variants, *args, **kwargs)
        else:
            result = metric(self.variants, *args, **kwargs)
        return result

