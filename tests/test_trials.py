from nose import tools

from trials.trials import *


class TestTrials:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C', 'D', 'E'])

    def test_raises_unknown_dtype(self):
        tools.assert_raises(Trials.UnsupportedVariationType,
                            Trials, ['A', 'B'], 'whatever')

    def test_raises_unknown_statistic(self):
        tools.assert_raises(Trials.UnsupportedStatistic,
                            self.trials.evaluate, 'whatever')

    def test_variants(self):
        tools.assert_true(len(self.trials.variations) == 5)

    def test_update(self):
        self.trials.update({'A': (1000, 500), 'B': (1000, 500)})
