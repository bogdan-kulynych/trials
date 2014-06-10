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

    result = test.evaluate('lift')
    print(result)