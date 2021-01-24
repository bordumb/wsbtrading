#!/usr/bin/env python
import sys
from setuptools import setup
import setuptools

import wsbtrading

with open('README.md', 'r', encoding='utf-8') as readme:
    DESCRIPTION = readme.read()

version = wsbtrading.__version__

for arg in sys.argv:
    if arg.startswith(wsbtrading.__version__):
        staging_version = sys.argv[2]
        version = staging_version
        sys.argv.remove(staging_version)
        break

DISTNAME = 'wsbtrading'
DESCRIPTION = """wsbtrading is a library that handles data I/O, aggregation, 
and modeling to facilitate algorithmic trading stategies."""
MAINTAINER = 'Brian Deely'
MAINTAINER_EMAIL = 'brian.s.deely@gmail.com'
AUTHOR = 'Brian Deely'
AUTHOR_EMAIL = 'brian.s.deely@gmail.com'
URL = "https://github.com/bordumb/wsbtrading"
LICENSE = "Apache License, Version 2.0"

classifiers = ['Programming Language :: Python',
               'Programming Language :: Python :: 3.6',
               'Intended Audience :: Science/Research',
               'Topic :: Scientific/Engineering',
               'Topic :: Scientific/Engineering :: Mathematics',
               'Operating System :: OS Independent']

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        version=version,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        packages=setuptools.find_packages(),
        classifiers=classifiers,
        test_suite='nose.collector',
    )
