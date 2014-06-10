import sys
sys.path.append('..')

from trials import Trials


if __name__ == '__main__':
    test = Trials(['A', 'B', 'C'])

    test.update({
        'A': (50, 10),
        'B': (45, 10),
        'C': (20, 20)
    })

    print(test.summary)