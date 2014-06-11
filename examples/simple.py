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

    lift = test.evaluate('lift', control='A')
    domination = test.evaluate('domination', control='A')

    for variation in ['B', 'C']:
        print('Variation {name}:'.format(name=variation))
        print('* lift = {value:.2%}'.format(value=lift[variation]))
        print('* P({name} > {control}) = {value:.2%}' \
            .format(name=variation, control='A', value=domination[variation]))