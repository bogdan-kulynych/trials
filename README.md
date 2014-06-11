trials
======
Tiny Bayesian A/B testing library

[![Build Status](https://travis-ci.org/bogdan-kulynych/trials.svg?branch=master)](https://travis-ci.org/bogdan-kulynych/trials)

### Install:

```
pip install -r requirements.txt
```

Also pip might not install all the system packages needed for scipy. To install them on Debian:

```
sudo apt-get install libatlas-dev libatlas-base-dev liblapack-dev gfortran
```

Run tests:

```
nosetests
```

### Usage

```python
# Start an A/B test with Bernoulli (binary) observations
test = Trials(['A', 'B', 'C'])

# Observe successes and failures
test.update({
    'A': (50, 10), # 50 successes, 10 failures, total 60
    'B': (75, 15), # 75 successes, 15 failures, total 90
    'C': (20, 15)  # 20 successes, 15 failures, total 35
})

print(test.evaluate('lift'))
print(test.evaluate('domination'))
```

Output:
```
B: lift = 0.86%
C: lift = -30.39%
B: p = 50.32%
C: p = 0.22%
```

This means that variant **B** is better than **A** by about 0.8% (*lift*) with 50% (*p*) chance, and variant **C** is worse than **A** by 30% with 1 - 0.2 = 99.8% chance, given that statistical assumptions on independence and identical Bernoulli distributions hold.

### Theory
See how Bayesian metrics (blue) compare to Frequentist ones (green) in the [notebook](http://nbviewer.ipython.org/github/bogdan-kulynych/trials/blob/master/examples/benchmark.ipynb).