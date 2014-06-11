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

    print('LIFT')
    lift = test.evaluate('lift')
    print(lift)

    print('DOMINATION')
    domination = test.evaluate('domination')
    print(domination)

    print('FREQUENTIST DOMINATION')
    f_domination = test.evaluate('z-test')
    print(f_domination)