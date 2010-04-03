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
from nose.tools import assert_equals
from os.path import dirname, abspath, join
from lettuce.fs import FeatureFinder

def test_feature_finder_finds_all_feature_files_within_a_dir():
    "FeatureFinder finds all feature files within a directory"
    current_dir = abspath(dirname(__file__))

    ff = FeatureFinder(current_dir)
    files = ff.find_feature_files()

    cjoin = lambda *x: join(current_dir, *x)
    assert_equals(
        sorted(files),
        sorted([
            cjoin('1st_feature_dir', 'one_more.feature'),
            cjoin('1st_feature_dir', 'some.feature'),
            cjoin('1st_feature_dir', 'more_features_here', 'another.feature'),
        ])
    )
