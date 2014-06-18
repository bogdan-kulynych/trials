import sys
sys.path.append('..')

from trials import Trials


if __name__ == '__main__':
    test = Trials(['A', 'B', 'C'])

    test.update({
        'A': (50, 10),
        'B': (75, 15),
        'C': (20, 15)
    })

    dominance = test.evaluate('dominance', control='A')
    lift = test.evaluate('lift', control='A')
    interval = test.evaluate('lift CI', control='A', ci=95)

    for variation in ['B', 'C']:
        print('Variation {name}:'.format(name=variation))
        print('* E[lift] = {value:.2%}'.format(value=lift[variation]))
        print('* P({lower:.2%} < lift < {upper:.2%}) = 95%' \
            .format(lower=interval[variation][0], upper=interval[variation][2]))
        print('* P({name} > {control}) = {value:.2%}' \
            .format(name=variation, control='A', value=dominance[variation]))