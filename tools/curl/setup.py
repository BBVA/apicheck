from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name="gurl",
    packages=find_packages(),
    install_requires=required
)