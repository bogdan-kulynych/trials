from setuptools import setup
from pip.req import parse_requirements

parsed_reqs = parse_requirements('requirements.txt')
requirements = [str(x.req) for x in parsed_reqs]


setup (name='trials',
       version='0.1',
       description='Tiny Bayesian A/B testing library',
       author='Bogdan Kulynych',
       author_email='hello@hidden-markov.com',
       url='https://github.com/trials',
       packages=['trials', 'trials.tests'],
       license='MIT',
       keywords='A/B testing, data analysis, statistics',
       classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
        ],
        install_requires=requirements,
        test_suite='nose.collector',
        test_requires=[
            'nose'
        ])
