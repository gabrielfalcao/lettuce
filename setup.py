#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
from setuptools import setup


def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('lettuce'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

required_modules = ['sure', 'fuzzywuzzy', 'python-subunit']

if sys.version_info[:2] < (2, 6):
    required_modules.append('multiprocessing')

if os.name.lower() == 'nt':
    required_modules.append('colorama')

setup(
    name='lettuce',
    version='0.2.21',
    description='Behaviour Driven Development for python',
    author='Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='http://lettuce.it',
    packages=get_packages(),
    install_requires=required_modules,
    entry_points={
        'console_scripts': ['lettuce = lettuce.bin:main'],
        },
    package_data={
        'lettuce': ['COPYING', '*.md'],
    },
)
