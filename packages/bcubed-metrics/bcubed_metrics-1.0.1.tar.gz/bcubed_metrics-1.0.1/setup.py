from setuptools import setup, find_packages

NAME = 'bcubed-metrics'
VERSION = '1.0.1' 
DESCRIPTION = 'A package to calculate BCUBED precision, recall, and F1-score for clustering evaluation.'
URL = 'https://github.com/nezumiCodes/bcubed-metrics'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author='Vasiliki Nikolaidi',
    url=URL,
    packages=find_packages(),
    keywords=['bcubed'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
