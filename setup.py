#!/usr/bin/env python
import pathlib
import subprocess
import sys

from setuptools import setup, find_packages

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

def _get_sha() -> str:
    """Takes the sha from the HEAD commit."""
    project_root = pathlib.Path(__file__).parent
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=project_root).decode('ascii').strip()

    except subprocess.CalledProcessError:  # most likely runs from tox
        pass

for arg in sys.argv:
    if arg == 'dev-build':
        sha = _get_sha()
        if sha is not None:
            _hash = _get_sha()[:7]
            version += '+' + _hash
        sys.argv.remove(arg)
        break

DISTNAME = 'wsbtrading'
DESCRIPTION = """wsbtrading is a library that handles data I/O, aggregation,
and modeling to facilitate algorithmic trading stategies."""
MAINTAINER = 'bordumb'
# MAINTAINER_EMAIL = 'DM me here or on Reddit: @bordumb'
AUTHOR = 'bordumb'
AUTHOR_EMAIL = 'DM me here or on Reddit: @bordumb'
URL = "https://github.com/bordumb/wsbtrading"
LICENSE = "Apache License, Version 2.0"

classifiers = ['Programming Language :: Python',
               'Programming Language :: Python :: 3.6',
               'Intended Audience :: Science/Research',
               'Topic :: Scientific/Engineering',
               'Topic :: Scientific/Engineering :: Mathematics',
               'Operating System :: OS Independent',
               'Intended Audience :: Financial and Insurance Industry',
               'Intended Audience :: Information Technology']

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        version=version,
        maintainer=MAINTAINER,
        # maintainer_email=MAINTAINER_EMAIL,
        description='wsbtrading is a library that handles data I/O, aggregation, and modeling to facilitate algorithmic trading stategies.',
        long_description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        packages=find_packages(),
        classifiers=classifiers,
        test_suite='nose.collector',
    )
