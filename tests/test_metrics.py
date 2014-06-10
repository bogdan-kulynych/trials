from nose import tools

from trials.trials import *
from trials.metrics import *


class TestLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.lift = self.trials.evaluate('lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.lift.result) == 2)

    def test_str(self):
        str(self.lift)

    def test_sanity(self):
        tools.assert_true(self.lift.result['C']['lift'] < 0 and \
            self.lift.result['B']['lift'] < 0)
        tools.assert_true(self.lift.result['C']['lift'] > \
            self.lift.result['B']['lift'])
