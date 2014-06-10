trials
======
## Bayesian A/B testing thing

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
# Starts an A/B test with Bernoulli (Binary) observations
test = Trials(['A', 'B', 'C'])

# Add info on successes and failures
test.update({
    'A': (50, 10),
    'B': (45, 10),
    'C': (20, 20)
})

print(test.summary)
```

Output:
```
(lift)
B: lift = -1.57%, p = 58.53%
C: lift = -39.21%, p = 99.87%
```

This means that variant **B** is worse than **A** by about 1.57% (*lift*) with 58.53% (*p*) chance, and variant **C** is worse than **A** by 39.21% with 99.87% chance, given that statistical assumptions on independence and identical Bernoulli distributions hold.