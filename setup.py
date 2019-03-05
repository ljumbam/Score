import setuptools
from distutils.core import setup

DESCRIPTION = 'A tool for writing music.'

setup(
    name='score',
    version='0.0.1',
    author='Loayeh Jumbam',
    author_email='loayeh@algotunes.com',
    packages=setuptools.find_packages(),
    license=open('LICENSE.txt'),
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    install_requires=[
        'mido'
    ]
)
