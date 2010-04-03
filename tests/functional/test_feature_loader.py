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
from lettuce.fs import FeatureLoader
from lettuce.core import Feature

current_dir = abspath(dirname(__file__))
cjoin = lambda *x: join(current_dir, *x)

def test_feature_finder_finds_all_feature_files_within_a_dir():
    "FeatureLoader finds all feature files within a directory"

    ff = FeatureLoader(current_dir)
    files = ff.find_feature_files()

    assert_equals(
        sorted(files),
        sorted([
            cjoin('1st_feature_dir', 'one_more.feature'),
            cjoin('1st_feature_dir', 'some.feature'),
            cjoin('1st_feature_dir', 'more_features_here', 'another.feature'),
        ])
    )

def test_feature_finder_loads_feature_objects():
    "Feature.from_file loads feature by filename"

    feature_file = cjoin('1st_feature_dir', 'more_features_here', 'another.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(type(feature), Feature)
    expected_scenario_names = ["Regular numbers", "Fractions"]
    got_scenario_names = [s.name for s in feature.scenarios]

    assert_equals(expected_scenario_names, got_scenario_names)
    assert_equals(len(feature.scenarios[0].steps), 4)

    step1, step2, step3, step4 = feature.scenarios[0].steps

    assert_equals(step1.sentence, '* I have entered 3 into the calculator')
    assert_equals(step2.sentence, '* I have entered 2 into the calculator')
    assert_equals(step3.sentence, '* I press divide')
    assert_equals(step4.sentence, '* the result should be 1.5 on the screen')

def test_feature_loaded_from_file_has_feature_line_and_feature_filename():
    "Feature.from_file sets FeatureDefinition into Feature objects, " \
    "giving line number and filename as well"

    feature_file = cjoin('1st_feature_dir', 'more_features_here', 'another.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(feature.defined_at.file, feature_file)
    assert_equals(feature.defined_at.line, 2)

def test_scenario_loaded_from_file_sets_scenario_line_and_scenario_filename():
    "Feature.from_file sets ScenarioDefinition into Scenario objects, " \
    "giving line number and filename as well"

    feature_file = cjoin('1st_feature_dir', 'more_features_here', 'another.feature')

    feature = Feature.from_file(feature_file)
    scenario1, scenario2 = feature.scenarios

    assert_equals(scenario1.defined_at.file, feature_file)
    assert_equals(scenario1.defined_at.line, 6)

    assert_equals(scenario2.defined_at.file, feature_file)
    assert_equals(scenario2.defined_at.line, 12)
