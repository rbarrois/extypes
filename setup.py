#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011-2013 Raphaël Barrois
# This code is distributed under the two-clause BSD License.

import codecs
import os
import re
import sys

from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    init_path = os.path.join(root_dir, *(package_components + ['__init__.py']))
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


PACKAGE = 'extypes'


setup(
    name=PACKAGE,
    version=get_version(PACKAGE),
    description="Enhancements over Python's standard types",
    author="Raphaël Barrois",
    author_email="raphael.barrois+%s@polytechnique.org" % PACKAGE,
    url='https://github.com/rbarrois/%s' % PACKAGE,
    keywords=['types', 'datastructure', 'structure'],
    packages=[PACKAGE],
    license='BSD',
    setup_requires=[
        'setuptools>=0.8',
    ],
    tests_require=[
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    test_suite='tests',
)
