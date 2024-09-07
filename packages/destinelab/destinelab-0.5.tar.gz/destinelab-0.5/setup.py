from setuptools import setup, find_packages

setup(
    name='destinelab',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
    ],
)
