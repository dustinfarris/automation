#!/usr/bin/env python
"""
Automation
==========

Automation is a Django-specific implementation of Fabric that provides
automation for server and git repository tasks.

:copyright: (c) 2013 by Dustin Farris
:license: BSD, see LICENSE for more details

"""

from setuptools import setup, find_packages


tests_require = []

install_requires = [
  'Django>=1.4,<1.5',
  'Fabric==1.5.2']

setup(
  name='automation',
  version='0.3.3.1',
  author='Dustin Farris',
  author_email='dustin@dustinfarris.com',
  url='https://github.com/dustinfarris/automation',
  description='A Django-specific implementation of Fabric',
  long_description=__doc__,
  package_dir={'': 'src'},
  packages=find_packages('src'),
  zip_safe=False,
  install_requires=install_requires,
  tests_require=tests_require,
  test_suite='runtests.runtests',
  license='BSD',
  include_package_data=True,
  classifiers=[
    'Framework :: Django',
    'Intended Audience :: System Administrators',
    'Operating System :: Unix',
    'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    'Topic :: Software Development :: Version Control',
    'Topic :: Software Development :: Quality Assurance'])
