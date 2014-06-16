from collections import OrderedDict

from .variations import vtypes as default_vtypes
from .metrics import metrics as default_metrics


class Trials(object):
    """
    Main interface for creating A/B tests.
    """
    class UnsupportedVariationType(Exception):
        pass

    class UnsupportedMetric(Exception):
        pass

    def __init__(self, variant_labels, vtype='bernoulli', *args, **kwargs):
        if isinstance(vtype, str):
            if vtype not in default_vtypes:
                raise Trials.UnsupportedVariationType(vtype)
            vtype = default_vtypes[vtype]

        self.vtype = vtype
        self.variations = OrderedDict([(label, vtype(*args, **kwargs)) \
            for label in variant_labels])

    def update(self, feed):
        for label, observations in feed.items():
            self.variations[label].update(*observations)

    def evaluate(self, metric, *args, **kwargs):
        result = None
        if isinstance(metric, str):
            if metric not in self.vtype.metrics:
                raise Trials.UnsupportedMetric(metric)
            func = default_metrics[metric]
            result = func(self.variations, *args, **kwargs)
        else:
            result = metric(self.variations, *args, **kwargs)
        return result