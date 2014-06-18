from nose import tools

from trials.trials import *
from trials.metrics import *


class TestLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)

    def test_str(self):
        str(self.metric)

    def test_sanity(self):
        tools.assert_true(self.metric['C'] < 0 and \
            self.metric['B'] < 0)
        tools.assert_true(self.metric['C'] > \
            self.metric['B'])


class TestDominance:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('dominance', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)

    def test_str(self):
        str(self.metric)

    def test_sanity(self):
        tools.assert_true(self.metric['C'] > \
            self.metric['B'])


class TestFrequentistDominance:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('z-test dominance', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)

    def test_str(self):
        str(self.metric)

    def test_sanity(self):
        tools.assert_true(self.metric['C'] > \
            self.metric['B'])


class TestEmpiricalLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('empirical lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)

    def test_str(self):
        str(self.metric)

    def test_sanity(self):
        tools.assert_true(self.metric['C'] < 0 and \
            self.metric['B'] < 0)
        tools.assert_true(self.metric['C'] > \
            self.metric['B'])