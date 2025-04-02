from setuptools import setup, find_packages

setup(
    name='postgres',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'numpy>=1.19.5',
        'pandas>=1.2.0',
        'django>=5.1.3',
    ],
)