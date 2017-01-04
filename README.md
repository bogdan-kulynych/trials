trials
======
Tiny Bayesian A/B testing library

[![Build Status](https://travis-ci.org/bogdan-kulynych/trials.svg?branch=master)](https://travis-ci.org/bogdan-kulynych/trials) [![Code Health](https://landscape.io/github/bogdan-kulynych/trials/master/landscape.svg?style=flat)](https://landscape.io/github/bogdan-kulynych/trials/master)

## Installation


Install system dependencies (Debian):

```
sudo apt-get install libatlas-dev libatlas-base-dev liblapack-dev gfortran
```

Install the Python package:

```
pip install git+git://github.com/bogdan-kulynych/trials.git@master
```

Run the tests:

```
nosetests trials/tests
```

## Usage

Import package

```python
from trials import Trials
```

Start a split test with Bernoulli (binary) observations
```python
test = Trials(['A', 'B', 'C'])
```

Observe successes and failures
```python
test.update({
    'A': (50, 10), # 50 successes, 10 failures, total 60
    'B': (75, 15), # 75 successes, 15 failures, total 90
    'C': (20, 15)  # 20 successes, 15 failures, total 35
})
```

Evaluate some statistics
```python
dominances = test.evaluate('dominance', control='A')         # Dominance probabilities P(X > A)
lifts = test.evaluate('expected lift', control='A')          # Expected lifts E[(X-A)/A]
intervals = test.evaluate('lift CI', control='A', level=95)  # Lifts' 95%-credible intervals
```

Available statistics for Bernoulli observation variations: `expected posterior`, `posterior CI`, `expected lift`, `lift CI`, `empirical lift`, `dominance`, `z-test dominance`.

Print or visualize results
```python
for variation in ['B', 'C']:
    print('Variation {name}:'.format(name=variation))
    print('* E[lift] = {value:.2%}'.format(value=lifts[variation]))
    print('* P({lower:.2%} < lift < {upper:.2%}) = 95%' \
        .format(lower=intervals[variation][0], upper=intervals[variation][2]))
    print('* P({name} > {control}) = {value:.2%}' \
        .format(name=variation, control='A', value=dominances[variation]))
```

Examine the output:
```
Variation B:
* E[lift] = 0.22%                       # expected lift
* P(-13.47% < lift < 17.31%) = 95%      # lift CI
* P(B > A) = 49.27%                     # dominance
Variation C:
* E[lift] = -31.22%
* P(-51.33% < lift < -9.21%) = 95%
* P(C > A) = 0.25%
```

#### Interpreting and analyzing results

As per the output above there's 50% chance that variation **B** is better than **A** (*dominance*). Most likely it is better by about 0.2% (*expected lift*), but there's 95% chance that real lift is anywhere betwen -13% to 17% (*lift CI*). You need more data to know if **B** is better or worse for sure.

There's 100% - 0.25% = 99.75% chance that variation **C** is worse than **A**. Most likely it is worse by about 31%, and there's 95% chance that real lift falls betwen -51% to -9%. The data was sufficient to tell that this variation is almost certainly inferior to both **A** and **B**. However, if this 99.75% chance still doesn't convince you, you need more data.

## Theory
Explanation of mathematics behind and usage guide are coming soon as a blog post.

Meanwhile, see the [notebook](http://nbviewer.ipython.org/github/bogdan-kulynych/trials/blob/master/examples/benchmark.ipynb) for comparison of Bayesian lift (blue) and empirical lift (green) errors in a theoretical benchmark with equal sample sizes. Bayesian approach is a little better at predicting the lift, but no miracles here. Bayesian p-values and frequentist (z-test) p-values yield almost identical results.
