try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='zdravomil',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/user-cont/zdravomil'
)
