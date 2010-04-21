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
import sys
from StringIO import StringIO

from os.path import dirname, abspath, join
from nose.tools import assert_equals, with_setup

from lettuce import Runner
from lettuce.fs import FeatureLoader
from lettuce.core import Feature

current_dir = abspath(dirname(__file__))
cjoin = lambda *x: join(current_dir, *x)

def prepare_stdout():
    if isinstance(sys.stdout, StringIO):
        del sys.stdout

    std = StringIO()
    sys.stdout = std

def assert_stdout(expected):
    string = sys.stdout.getvalue()
    assert_equals(string, expected)

def assert_lines(one, other):
    for line1, line2 in zip(one.splitlines(), other.splitlines()):
        assert_equals(line1, line2)

def test_feature_representation_without_colors():
    "Feature represented without colors"
    feature_file = cjoin('1st_feature_dir', 'some.feature')

    feature = Feature.from_file(feature_file)
    assert_lines(
        feature.represented(color=False),
        "Feature: Addition                                      # tests/functional/1st_feature_dir/some.feature:5\n"
        "  In order to avoid silly mistakes                     # tests/functional/1st_feature_dir/some.feature:6\n"
        "  As a math idiot                                      # tests/functional/1st_feature_dir/some.feature:7\n"
        "  I want to be told the sum of two numbers             # tests/functional/1st_feature_dir/some.feature:8\n"
    )

def _test_scenario_representation_without_colors():
    "Scenario represented without colors"
    feature_file = cjoin('1st_feature_dir', 'some.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(
        feature.scenarios[0].represented(color=False),
        "  Scenario Outline: Add two numbers                    # tests/functional/1st_feature_dir/some.feature:10\n"
    )

def _test_undefined_step_representation_without_colors():
    "Undefined step represented without colors"
    feature_file = cjoin('runner_features', 'first.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(
        feature.scenarios[0].steps[0].represented(color=False),
        "     Given I do nothing                    # tests/functional/runner_features/first.feature:7\n"
    )
    assert_equals(
        feature.scenarios[0].steps[1].represented(color=False),
        "     Then I see that the test passes       # tests/functional/runner_features/first.feature:8\n"
    )

def _test_defined_step_representation_without_colors():
    "Defined step represented without colors"
    feature_file = cjoin('runner_features', 'first.feature')
    loader = FeatureLoader('runner_features')
    loader.find_and_load_step_definitions()

    feature = Feature.from_file(feature_file)

    assert_equals(
        feature.scenarios[0].solved_steps[0].represented(color=False),
        "     Given I do nothing                    # tests/functional/runner_features/dumb_steps.py:6\n"
    )
    assert_equals(
        feature.scenarios[0].solved_steps[1].represented(color=False),
        "     Then I see that the test passes       # tests/functional/runner_features/dumb_steps.py:7\n"
    )

@with_setup(prepare_stdout)
def _test_output_with_success_colorless():
    "Testing the output of a successful feature"

    runner = Runner(join(abspath(dirname(__file__)), 'runner_features'), verbosity=3)
    runner.run()

    assert_stdout(
    "Feature: Dumb feature                     # tests/functional/runner_features/first.feature: 1\n"
    "  In order to test success\n"
    "  As a programmer\n"
    "  I want to see that the output is green\n"
    "\n"
    "  Scenario: Do nothing                    # tests/functional/runner_features/first.feature: 6\n"
    "    Given I do nothing                    # tests/functional/runner_features/dumb_steps.py: 6\n"
    "    Then I see that the test passes       # tests/functional/runner_features/dumb_steps.py: 8\n"
    )
