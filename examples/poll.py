"""Sociological poll example."""

import sys
sys.path.append('..')

from trials import Trials


if __name__ == '__main__':
    test = Trials(['Poroshenko', 'Tymoshenko'])

    test.update({
        'Poroshenko': (48, 52),
        'Tymoshenko': (12, 88)
    })

    estimates = test.evaluate('posterior CI')
    dominance = test.evaluate('dominance', control='Tymoshenko')

    print('Poroshenko estimated vote share: {lower:.2%} - {upper:.2%} '
          '(95% credibility)'
          .format(lower=estimates['Poroshenko'][0],
                  upper=estimates['Poroshenko'][2]))

    print('Tymoshenko estimated vote share: {lower:.2%} - {upper:.2%} '
          '(95% credibility)'
          .format(lower=estimates['Tymoshenko'][0],
                  upper=estimates['Tymoshenko'][2]))

    print('Chance that Poroshenko beats Tymoshenko based on the poll data: '
          '{chance:.2%}'.format(chance=dominance['Poroshenko']))
