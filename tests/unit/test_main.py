# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
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

import lettuce
from nose.tools import assert_equals
from mox import Mox

def test_has_version():
    "A nice python module is supposed to have a version"
    assert_equals(lettuce.version, '0.1rc8')

def test_import():
    "lettuce importer does import"
    import os
    module = lettuce._import('os')
    assert_equals(os, module)

def test_terrain_import_exception():
    "lettuce error tries to import "
    string = 'Lettuce has tried to load the conventional environment ' \
        'module "terrain"\nbut it has errors, check its contents and ' \
        'try to run lettuce again.\n'

    mox = Mox()

    mox.StubOutWithMock(lettuce, '_import')
    mox.StubOutWithMock(lettuce, 'fs')
    mox.StubOutWithMock(lettuce.fs, 'FileSystem')
    mox.StubOutWithMock(lettuce.sys, 'stderr')
    mox.StubOutWithMock(lettuce.sys, 'path')

    lettuce._import('terrain').AndRaise(Exception('foo bar'))

    lettuce.fs.FeatureLoader("[some path]")
    lettuce.sys.stderr.write(string)
    lettuce.sys.path.insert(0, '[some path]')

    mox.ReplayAll()

    try:
        lettuce.Runner("[some path]")
    except SystemExit:
        mox.VerifyAll()
