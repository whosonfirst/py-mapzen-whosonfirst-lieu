#!/usr/bin/env python

# Remove .egg-info directory if it exists, to avoid dependency problems with
# partially-installed packages (20160119/dphiffer)

import os, sys
from shutil import rmtree

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
egg_info = cwd + "/mapzen.whosonfirst.utils.egg-info"
if os.path.exists(egg_info):
    rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
version = open("VERSION").read()
desc = open("README.md").read()

setup(
    name='mapzen.whosonfirst.lieu',
    namespace_packages=['mapzen', 'mapzen.whosonfirst'],
    version=version,
    description='Who\'s On First utilities for working with the lieu toolchain.',
    author='Mapzen',
    url='https://github.com/whosonfirst/py-mapzen-whosonfirst-lieu',
    packages=packages,
    scripts=[
        'scripts/lieu-dupes-filter',
        'scripts/lieu-dupes-process',
        'scripts/lieu-dupes-report',
        'scripts/lieu-fetch-postalcodes',
        'scripts/lieu-translate-ldngov-dlb',
        'scripts/lieu-translate-nycgov-lob',
        'scripts/lieu-translate-nycgov-dohmh',
        'scripts/lieu-translate-openaddresses',
        'scripts/lieu-translate-sfgov-rbl',
        'scripts/lieu-translate-socrata',
        'scripts/lieu-validate',
        ],
    download_url='https://github.com/whosonfirst/py-mapzen-whosonfirst-lieu/releases/tag/' + version,
    license='BSD')
