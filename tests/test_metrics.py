from nose import tools

from trials.trials import *
from trials.metrics import *


class TestLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric.values) == 2)

    def test_str(self):
        str(self.metric)

    def test_sanity(self):
        tools.assert_true(self.metric.values['C'] < 0 and \
            self.metric.values['B'] < 0)
        tools.assert_true(self.metric.values['C'] > \
            self.metric.values['B'])


class TestDomination:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('domination', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric.values) == 2)

    def test_str(self):
        str(self.metric)

    def test_sanity(self):
        tools.assert_true(self.metric.values['C'] > \
            self.metric.values['B'])


class TestFrequentistDomination:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('frequentist domination', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric.values) == 2)

    def test_str(self):
        str(self.metric)

    def test_sanity(self):
        tools.assert_true(self.metric.values['C'] > \
            self.metric.values['B'])