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
from os.path import dirname, join, abspath
from lettuce.fs import FeatureLoader
from lettuce.core import Feature, fs

current_dir = abspath(dirname(__file__))
cjoin = lambda *x: join(current_dir, 'simple_features', *x)

def test_feature_finder_finds_all_feature_files_within_a_dir():
    "FeatureLoader finds all feature files within a directory"

    ff = FeatureLoader(cjoin())
    files = ff.find_feature_files()

    assert_equals(
        sorted(files),
        sorted([
            cjoin('1st_feature_dir', 'one_more.feature'),
            cjoin('1st_feature_dir', 'some.feature'),
            cjoin('1st_feature_dir', 'more_features_here', 'another.feature'),
            cjoin('2nd_feature_dir', 'before_and_after_all.feature'),
            cjoin('2nd_feature_dir', 'with_defined_steps.feature'),
            cjoin('3rd_feature_dir', 'my_steps_are_anywhere.feature'),
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
    "Feature.from_file sets FeatureDescription into Feature objects, " \
    "giving line number and filename as well"

    feature_file = cjoin('1st_feature_dir', 'more_features_here', 'another.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(feature.described_at.file, fs.relpath(feature_file))
    assert_equals(feature.described_at.line, 2)
    assert_equals(feature.name, 'Division')
    assert_equals(feature.described_at.description_at, (3, 4))

def test_feature_loaded_from_file_has_description_at():
    "Feature.from_file sets FeatureDescription with line numbers of its description"

    feature_file = cjoin('1st_feature_dir', 'some.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(feature.described_at.file, fs.relpath(feature_file))
    assert_equals(feature.described_at.line, 5)
    assert_equals(feature.name, 'Addition')
    assert_equals(feature.described_at.description_at, (6, 7, 8))
    assert_equals(
        feature.description,
        "In order to avoid silly mistakes\n"
        "As a math idiot\n"
        "I want to be told the sum of two numbers"
    )

def test_feature_loaded_from_file_sets_scenario_line_and_scenario_filename():
    "Feature.from_file sets ScenarioDescription into Scenario objects, " \
    "giving line number and filename as well"

    feature_file = cjoin('1st_feature_dir', 'more_features_here', 'another.feature')

    feature = Feature.from_file(feature_file)
    scenario1, scenario2 = feature.scenarios

    assert_equals(scenario1.described_at.file, fs.relpath(feature_file))
    assert_equals(scenario1.described_at.line, 6)

    assert_equals(scenario2.described_at.file, fs.relpath(feature_file))
    assert_equals(scenario2.described_at.line, 12)

def test_feature_loaded_from_file_sets_step_line_and_step_filenames():
    "Feature.from_file sets StepDescription into Scenario objects, " \
    "giving line number and filename as well"

    feature_file = cjoin('1st_feature_dir', 'one_more.feature')

    feature = Feature.from_file(feature_file)
    (scenario, ) = feature.scenarios

    step1, step2, step3, step4 = scenario.steps

    for step in scenario.steps:
        assert_equals(step.described_at.file, fs.relpath(feature_file))

    assert_equals(step1.sentence, "* I have entered 10 into the calculator")
    assert_equals(step1.described_at.line, 7)

    assert_equals(step2.sentence, "* I have entered 4 into the calculator")
    assert_equals(step2.described_at.line, 8)

    assert_equals(step3.sentence, "* I press multiply")
    assert_equals(step3.described_at.line, 9)

    assert_equals(step4.sentence, "* the result should be 40 on the screen")
    assert_equals(step4.described_at.line, 10)
