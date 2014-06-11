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

    print('EMPIRICAL LIFT')
    e_lift = test.evaluate('empirical lift')
    print(e_lift)

    print('FREQUENTIST DOMINATION')
    f_domination = test.evaluate('frequentist domination')
    print(f_domination)