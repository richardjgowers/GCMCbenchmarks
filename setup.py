from setuptools import setup, find_packages

from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()


setup(
    name = 'gcmcbenchmarks',
    version = '0.0.1',
    long_description=long_description,

    packages=find_packages(),
    include_package_data=True,

    scripts = ['bin/make_dlm_sims.py'],
)
