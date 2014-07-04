from nose import tools

from trials.trials import *
from trials.stats import *


eps = 10e-3


class TestExpectedPosterior:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.statistic = self.trials.evaluate('expected posterior')

    def test_evaluate(self):
        tools.assert_true(len(self.statistic) == 3)

    def test_sanity(self):
        tools.assert_true(self.statistic['A'] > 0.99)
        tools.assert_true(np.abs(self.statistic['B'] - 0.66) < eps)
        tools.assert_true(self.statistic['C'] > 0.9)


class TestPosteriorCI:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.statistic = self.trials.evaluate('posterior CI')
        self.mean = self.trials.evaluate('expected posterior')

    def test_evaluate(self):
        tools.assert_true(len(self.statistic) == 3)

    def test_sanity(self):
        print(self.statistic['A'])
        tools.assert_true(
            self.statistic['A'][0] < self.statistic['A'][1] < self.statistic['A'][2])
        tools.assert_true(
            self.statistic['B'][0] < self.statistic['B'][1] < self.statistic['B'][2])
        tools.assert_true(
            self.statistic['C'][0] < self.statistic['C'][1] < self.statistic['C'][2])
        tools.assert_true(
            self.statistic['A'][0] < self.mean['A'] < self.statistic['A'][2])
        tools.assert_true(
            self.statistic['B'][0] < self.mean['B'] < self.statistic['B'][2])
        tools.assert_true(
            self.statistic['C'][0] < self.mean['C'] < self.statistic['C'][2])


class TestExpectedLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.statistic = self.trials.evaluate('expected lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.statistic) == 2)

    def test_sanity(self):
        tools.assert_true(self.statistic['C'] < 0 and
                          self.statistic['B'] < 0)
        tools.assert_true(self.statistic['C'] >
                          self.statistic['B'])

    def test_formula_matches_mcmc_result(self):
        a_samples = self.trials.variations['A'].posterior.rvs(size=10000)
        b_samples = self.trials.variations['B'].posterior.rvs(size=10000)
        mcmc_lift = np.mean((b_samples - a_samples) / a_samples)
        tools.assert_true(np.abs(mcmc_lift - self.statistic['B']) < eps)


class TestLiftCI:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.statistic = self.trials.evaluate('lift CI', control='A')
        self.lift = self.trials.evaluate('expected lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.statistic) == 2)
        tools.assert_true(len(self.statistic['B']) == 3)

    def test_sanity(self):
        tools.assert_true(
            self.statistic['B'][0] < self.statistic['B'][1] <
            self.statistic['B'][2])
        tools.assert_true(
            self.statistic['C'][0] < self.statistic['C'][1] <
            self.statistic['C'][2])
        tools.assert_true(
            self.statistic['B'][0] < self.lift['B'] < self.statistic['B'][2])
        tools.assert_true(
            self.statistic['C'][0] < self.lift['C'] < self.statistic['C'][2])


class TestDominance:

    def setup(self):
        observations = {'A': (10000, 10), 'B': (10000, 5000), 'C': (1000, 10)}

        self.jeffreys_trials = Trials(['A', 'B', 'C'])
        self.jeffreys_trials.update(observations)
        self.jeffreys_statistic = self.jeffreys_trials.evaluate('dominance',
                                                                control='A')

        self.uninform_trials = Trials(['A', 'B', 'C'], alpha=1, beta=1)
        self.uninform_trials.update(observations)
        self.uninform_statistic = self.uninform_trials.evaluate('dominance',
                                                                control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.jeffreys_statistic) == 2)
        tools.assert_true(len(self.uninform_statistic) == 2)

    def test_sanity(self):
        tools.assert_true(self.jeffreys_statistic['C'] >=
                          self.jeffreys_statistic['B'])
        tools.assert_true(self.uninform_statistic['C'] >=
                          self.uninform_statistic['B'])

    def test_uninformed_and_informed_results_match(self):
        print(self.jeffreys_statistic['C'], self.uninform_statistic['C'])
        tools.assert_true(np.abs(self.jeffreys_statistic['B'] -
                                 self.uninform_statistic['B']) <= eps)
        tools.assert_true(np.abs(self.jeffreys_statistic['C'] -
                                 self.uninform_statistic['C']) <= eps)


class TestZTestDominance:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.statistic = self.trials.evaluate('z-test dominance', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.statistic) == 2)

    def test_sanity(self):
        tools.assert_true(self.statistic['C'] > self.statistic['B'])


class TestEmpiricalLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.statistic = self.trials.evaluate('empirical lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.statistic) == 2)

    def test_sanity(self):
        tools.assert_true(self.statistic['C'] < 0 and self.statistic['B'] < 0)
        tools.assert_true(self.statistic['C'] > self.statistic['B'])
