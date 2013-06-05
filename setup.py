#!/usr/bin/env python
from setuptools import setup

entry_points = {'console_scripts':
                ['modsecurity-exception-factory = modsecurity_exception_factory.commands.command_modsecurity_exception_factory:main']
               }

setup(setup_requires=['d2to1'],
      tests_require = ['mock', 'nose'],
      test_suite = 'nose.collector',
      entry_points = entry_points,
      d2to1 = True)
