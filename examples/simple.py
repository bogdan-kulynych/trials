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
        print('Variation {}:'.format(variation))
        print('* lift = {:.2%}'.format(lift[variation]))
        print('* P({} > {}) = {:.2%}'.format(variation, 'A', domination[variation]))