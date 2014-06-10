from nose import tools

from trials.trials import *
from trials.metrics import *


class TestLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 500), 'B': (1000, 500)})

    def test_evaluate(self):
        e = self.trials.evaluate(control='A')
        tools.assert_true(len(e['lift']) == 2)

    def test_summary(self):
        s = self.trials.summary
        tools.assert_true(isinstance(s, str))

