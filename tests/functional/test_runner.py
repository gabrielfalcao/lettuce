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
import os
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

def prepare_stderr():
    if isinstance(sys.stderr, StringIO):
        del sys.stderr

    std = StringIO()
    sys.stderr = std

def assert_stderr(expected):
    string = sys.stderr.getvalue()
    assert_equals(string, expected)

def assert_lines(one, other):
    for line1, line2 in zip(one.splitlines(), other.splitlines()):
        assert_equals(line1, line2)

@with_setup(prepare_stderr)
def test_try_to_import_terrain():
    "Runner tries to import terrain, but has a nice output when it fail"
    sandbox_path = cjoin('sandbox')
    original_path = abspath(".")
    os.chdir(sandbox_path)

    try:
        Runner(".")
        raise AssertionError('The runner should raise ImportError !')
    except SystemExit:
        assert_stderr(
            'Lettuce has tried to load the conventional environment module ' \
            '"terrain"\n'
            'but it has errors, check its contents and try to run lettuce again.\n'
        )

    finally:
        os.chdir(original_path)

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

def test_scenario_outline_representation_without_colors():
    "Scenario Outline represented without colors"
    feature_file = cjoin('1st_feature_dir', 'some.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(
        feature.scenarios[0].represented(color=False),
        "  Scenario Outline: Add two numbers                    # tests/functional/1st_feature_dir/some.feature:10\n"
    )

def test_scenario_representation_without_colors():
    "Scenario represented without colors"
    feature_file = cjoin('runner_features', 'first.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(
        feature.scenarios[0].represented(color=False),
        "  Scenario: Do nothing                   # tests/functional/runner_features/first.feature:6\n"
    )

def test_undefined_step_represent_string():
    "Undefined step represented without colors"
    feature_file = cjoin('runner_features', 'first.feature')

    feature = Feature.from_file(feature_file)
    step = feature.scenarios[0].steps[0]
    assert_equals(
        step.represent_string(step.sentence, color=False),
        "    Given I do nothing                   # tests/functional/runner_features/first.feature:7\n"
    )

    assert_equals(
        step.represent_string("foo bar", color=False),
        "    foo bar                              # tests/functional/runner_features/first.feature:7\n"
    )

def test_defined_step_represent_string():
    "Defined step represented without colors"
    feature_file = cjoin('runner_features', 'first.feature')
    feature_dir = cjoin('runner_features')
    loader = FeatureLoader(feature_dir)

    loader.find_and_load_step_definitions()

    feature = Feature.from_file(feature_file)
    step = feature.scenarios[0].steps[0]
    step.run(True)

    assert_equals(
        step.represent_string(step.sentence, color=False),
        "    Given I do nothing                   # tests/functional/runner_features/dumb_steps.py:6\n"
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


