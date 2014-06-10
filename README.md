trials
======
Bayesian A/B testing thing

[![Build Status](https://travis-ci.org/bogdan-kulynych/trials.svg?branch=master)](https://travis-ci.org/bogdan-kulynych/trials)

### Install:

```
pip install -r requirements.txt
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

print(test.summary)
```

Output:
```
(lift)
B: lift = 0.86%, p = 51.73%
C: lift = -30.39%, p = 99.53%
```

This means that variant **B** is better than **A** by about 0.8% (*lift*) with 51% (*p*) chance, and variant **C** is worse than **A** by 30% with 99.5% chance, given that statistical assumptions on independence and identical Bernoulli distributions hold.