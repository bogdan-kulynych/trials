trials
======
Tiny Bayesian A/B testing library

[![Build Status](https://travis-ci.org/bogdan-kulynych/trials.svg?branch=master)](https://travis-ci.org/bogdan-kulynych/trials)

### Install:

```
pip install -r requirements.txt
```

pip might not install all the system packages needed for scipy. To install them on Debian:

```
sudo apt-get install libatlas-dev libatlas-base-dev liblapack-dev gfortran
```

Running tests:

```
nosetests
```

### Usage

```python
from trials import Trials

# Start an A/B test with Bernoulli (binary) observations
test = Trials(['A', 'B', 'C'])

# Observe successes and failures
test.update({
    'A': (50, 10), # 50 successes, 10 failures, total 60
    'B': (75, 15), # 75 successes, 15 failures, total 90
    'C': (20, 15)  # 20 successes, 15 failures, total 35
})

# Evaluate results
lift = test.evaluate('lift', control='A')
dominance = test.evaluate('dominance', control='A')

# Print metrics
for variation in ['B', 'C']:
    print('Variation {name}:'.format(name=variation))
    print('* lift = {value:.2%}'.format(value=lift[variation]))
    print('* P({name} > {control}) = {value:.2%}' \
        .format(name=variation, control='A', value=dominance[variation]))
```

Output:
```
Variation B:
* lift = 0.22%
* P(B > A) = 50.39%
Variation C:
* lift = -31.22%
* P(C > A) = 0.35%
```

This means that variant **B** is better than **A** by about 0.2% (*lift*) with 50% (*p*) chance, and variant **C** is worse than **A** by 31% with 1 - 0.35 = 99.65% chance, given that statistical assumptions on independence and identical Bernoulli distributions hold.

### Theory
Explanation of mathematics behind and usage guide are coming soon as a blog post.

Meanwhile, see the [notebook](http://nbviewer.ipython.org/github/bogdan-kulynych/trials/blob/master/examples/benchmark.ipynb) for comparison of Bayesian lift (blue) and empirical lift (green) errors in a theoretical benchmark with equal sample sizes. Bayesian approach is a little better at predicting the lift, but no miracles here. Bayesian p-values and frequentist (z-test) p-values yield almost identical results.
