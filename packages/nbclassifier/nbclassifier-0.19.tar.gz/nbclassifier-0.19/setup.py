from setuptools import setup, find_packages

setup(
    name='nbclassifier',
    version='0.19',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn'
    ],
    author='Raghul',
    author_email='raghulares@gmail.com',
    description='a package that implements the naive bayesian classifier in a sample dataset'
    
)