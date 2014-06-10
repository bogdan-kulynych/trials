from nose import tools

from trials.trials import *


class TestTrials:

    def test_raises_unknown_dtype(self):
        tools.assert_raises(Trials.UnknownVtype, Trials, ['A', 'B'], \
            'whatever')

    def test_create_and_update(self):
        trials = Trials(['A', 'B', 'C', 'D', 'E'])
        tools.assert_true(len(trials.variants) == 5)
        trials.update({'A': (1000, 500), 'B': (1000, 500)})


