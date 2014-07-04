"""Trials class."""

from collections import OrderedDict

from .variations import vtypes as default_vtypes
from .stats import statistic_funcs


class Trials(object):

    """Main A/B test class."""

    class UnsupportedVariationType(Exception):
        pass

    class UnsupportedStatistic(Exception):
        pass

    def __init__(self, variation_labels, vtype='bernoulli', *args, **kwargs):
        """Create an A/B test assuming vtype variations."""
        if isinstance(vtype, str):
            if vtype not in default_vtypes:
                raise Trials.UnsupportedVariationType(vtype)
            vtype = default_vtypes[vtype]

        self.vtype = vtype
        self.variations = OrderedDict([(label, vtype(*args, **kwargs))
                                      for label in variation_labels])

    def update(self, feed):
        """Update test state with observations."""
        for label, observations in feed.items():
            self.variations[label].update(*observations)

    def evaluate(self, statistic, *args, **kwargs):
        """Evaluate a statistic."""
        result = None
        if isinstance(statistic, str):
            if statistic not in self.vtype.stats:
                raise Trials.UnsupportedStatistic(statistic)
            func = statistic_funcs[statistic]
            result = func(self.variations, *args, **kwargs)
        else:
            result = statistic(self.variations, *args, **kwargs)
        return result
