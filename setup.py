#!/usr/bin/env python
try:
      from setuptools import setup, find_packages
except ImportError:
      from distutils.core import setup

setup(name='FDSolver',
      version='0.2',
      description='Solver for Functional Dependencies',
      url='https://github.com/SimJunYou/FDSolver',
      author='Sim Jun You',
      author_email='simjunyou99@gmail.com',
      packages=find_packages(),
      license='MIT license',
      entry_points={
            'console_scripts': [
                  'fdsolver = fdsolver.ui:entry'
            ]
      }
) # TODO: Fill in the rest of the stuff if necessary
