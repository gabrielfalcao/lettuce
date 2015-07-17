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
import random
import lettuce
from mock import Mock, patch
from sure import expect
from StringIO import StringIO
from os.path import dirname, join, abspath
from inspect import currentframe

from nose.tools import assert_equals, with_setup, assert_raises
from lettuce.fs import FeatureLoader
from lettuce.core import Feature, fs, StepDefinition
from lettuce.terrain import world
from lettuce import Runner

from tests.asserts import assert_lines
from tests.asserts import prepare_stderr
from tests.asserts import prepare_stdout
from tests.asserts import assert_stderr_lines
from tests.asserts import assert_stdout_lines
from tests.asserts import assert_stderr_lines_with_traceback
from tests.asserts import assert_stdout_lines_with_traceback

current_dir = abspath(dirname(__file__))
lettuce_dir = abspath(dirname(lettuce.__file__))
ojoin = lambda *x: join(current_dir, 'output_features', *x)
sjoin = lambda *x: join(current_dir, 'syntax_features', *x)
tjoin = lambda *x: join(current_dir, 'tag_features', *x)
bjoin = lambda *x: join(current_dir, 'bg_features', *x)

lettuce_path = lambda *x: fs.relpath(join(lettuce_dir, *x))

call_line = StepDefinition.__call__.im_func.func_code.co_firstlineno + 5


def joiner(callback, name):
    return callback(name, "%s.feature" % name)


feature_name = lambda name: joiner(ojoin, name)
syntax_feature_name = lambda name: joiner(sjoin, name)
tag_feature_name = lambda name: joiner(tjoin, name)
bg_feature_name = lambda name: joiner(bjoin, name)


@with_setup(prepare_stderr)
def test_try_to_import_terrain():
    "Runner tries to import terrain, but has a nice output when it fail"
    sandbox_path = ojoin('..', 'sandbox')
    original_path = abspath(".")
    os.chdir(sandbox_path)

    try:
        import lettuce
        reload(lettuce)
        raise AssertionError('The runner should raise ImportError !')
    except SystemExit:
        assert_stderr_lines_with_traceback(
            'Lettuce has tried to load the conventional environment module '
            '"terrain"\nbut it has errors, check its contents and '
            'try to run lettuce again.\n\nOriginal traceback below:\n\n'
            "Traceback (most recent call last):\n"
            '  File "%(lettuce_core_file)s", line 44, in <module>\n'
            '    terrain = fs.FileSystem._import("terrain")\n'
            '  File "%(lettuce_fs_file)s", line 63, in _import\n'
            '    module = imp.load_module(name, fp, pathname, description)\n'
            '  File "%(terrain_file)s", line 18\n'
            '    it is here just to cause a syntax error\n'
            "                  ^\n"
            'SyntaxError: invalid syntax\n' % {
                'lettuce_core_file': abspath(join(lettuce_dir, '__init__.py')),
                'lettuce_fs_file': abspath(join(lettuce_dir, 'fs.py')),
                'terrain_file': abspath(lettuce_path('..', 'tests', 'functional', 'sandbox', 'terrain.py')),
            }
        )

    finally:
        os.chdir(original_path)


def test_feature_representation_without_colors():
    "Feature represented without colors"
    feature_file = ojoin('..', 'simple_features', '1st_feature_dir', 'some.feature')

    feature = Feature.from_file(feature_file)
    assert_lines(
        feature.represented(),
        "Feature: Addition                                      # tests/functional/simple_features/1st_feature_dir/some.feature:5\n"
        "  In order to avoid silly mistakes                     # tests/functional/simple_features/1st_feature_dir/some.feature:6\n"
        "  As a math idiot                                      # tests/functional/simple_features/1st_feature_dir/some.feature:7\n"
        "  I want to be told the sum of two numbers             # tests/functional/simple_features/1st_feature_dir/some.feature:8\n"
    )


def test_scenario_outline_representation_without_colors():
    "Scenario Outline represented without colors"
    feature_file = ojoin('..', 'simple_features', '1st_feature_dir', 'some.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(
        feature.scenarios[0].represented(),
        "  Scenario Outline: Add two numbers                    # tests/functional/simple_features/1st_feature_dir/some.feature:10\n"
    )


def test_scenario_representation_without_colors():
    "Scenario represented without colors"
    feature_file = ojoin('runner_features', 'first.feature')

    feature = Feature.from_file(feature_file)
    assert_equals(
        feature.scenarios[0].represented(),
        "  Scenario: Do nothing                   # tests/functional/output_features/runner_features/first.feature:6\n"
    )


def test_undefined_step_represent_string():
    "Undefined step represented without colors"
    feature_file = ojoin('runner_features', 'first.feature')

    feature = Feature.from_file(feature_file)
    step = feature.scenarios[0].steps[0]
    assert_equals(
        step.represent_string(step.sentence),
        "    Given I do nothing                   # tests/functional/output_features/runner_features/first.feature:7\n"
    )

    assert_equals(
        step.represent_string("foo bar"),
        "    foo bar                              # tests/functional/output_features/runner_features/first.feature:7\n"
    )


def test_defined_step_represent_string():
    "Defined step represented without colors"
    feature_file = ojoin('runner_features', 'first.feature')
    feature_dir = ojoin('runner_features')
    loader = FeatureLoader(feature_dir)
    world._output = StringIO()
    world._is_colored = False
    loader.find_and_load_step_definitions()

    feature = Feature.from_file(feature_file)
    step = feature.scenarios[0].steps[0]
    step.run(True)

    assert_equals(
        step.represent_string(step.sentence),
        "    Given I do nothing                   # tests/functional/output_features/runner_features/dumb_steps.py:6\n"
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorless2():
    "Testing the colorless output of a successful feature"

    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'runner_features'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        "\n"
        "Feature: Dumb feature                    # tests/functional/output_features/runner_features/first.feature:1\n"
        "  In order to test success               # tests/functional/output_features/runner_features/first.feature:2\n"
        "  As a programmer                        # tests/functional/output_features/runner_features/first.feature:3\n"
        "  I want to see that the output is green # tests/functional/output_features/runner_features/first.feature:4\n"
        "\n"
        "  Scenario: Do nothing                   # tests/functional/output_features/runner_features/first.feature:6\n"
        "    Given I do nothing                   # tests/functional/output_features/runner_features/dumb_steps.py:6\n"
        "\n"
        "1 feature (1 passed)\n"
        "1 scenario (1 passed)\n"
        "1 step (1 passed)\n"
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorless():
    "A feature with two scenarios should separate the two scenarios with a new line (in colorless mode)."

    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'many_successful_scenarios'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        "\n"
        "Feature: Dumb feature                    # tests/functional/output_features/many_successful_scenarios/first.feature:1\n"
        "  In order to test success               # tests/functional/output_features/many_successful_scenarios/first.feature:2\n"
        "  As a programmer                        # tests/functional/output_features/many_successful_scenarios/first.feature:3\n"
        "  I want to see that the output is green # tests/functional/output_features/many_successful_scenarios/first.feature:4\n"
        "\n"
        "  Scenario: Do nothing                   # tests/functional/output_features/many_successful_scenarios/first.feature:6\n"
        "    Given I do nothing                   # tests/functional/output_features/many_successful_scenarios/dumb_steps.py:6\n"
        "\n"
        "  Scenario: Do nothing (again)           # tests/functional/output_features/many_successful_scenarios/first.feature:9\n"
        "    Given I do nothing (again)           # tests/functional/output_features/many_successful_scenarios/dumb_steps.py:6\n"
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "2 steps (2 passed)\n"
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorful():
    "Testing the output of a successful feature"

    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'runner_features'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        "\n"
        "\033[1;37mFeature: Dumb feature                    \033[1;30m# tests/functional/output_features/runner_features/first.feature:1\033[0m\n"
        "\033[1;37m  In order to test success               \033[1;30m# tests/functional/output_features/runner_features/first.feature:2\033[0m\n"
        "\033[1;37m  As a programmer                        \033[1;30m# tests/functional/output_features/runner_features/first.feature:3\033[0m\n"
        "\033[1;37m  I want to see that the output is green \033[1;30m# tests/functional/output_features/runner_features/first.feature:4\033[0m\n"
        "\n"
        "\033[1;37m  Scenario: Do nothing                   \033[1;30m# tests/functional/output_features/runner_features/first.feature:6\033[0m\n"
        "\033[1;30m    Given I do nothing                   \033[1;30m# tests/functional/output_features/runner_features/dumb_steps.py:6\033[0m\n"
        "\033[A\033[1;32m    Given I do nothing                   \033[1;30m# tests/functional/output_features/runner_features/dumb_steps.py:6\033[0m\n"
        "\n"
        "\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 scenario (\033[1;32m1 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 step (\033[1;32m1 passed\033[1;37m)\033[0m\n"
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorful_newline():
    "A feature with two scenarios should separate the two scenarios with a new line (in color mode)."

    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'many_successful_scenarios'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        "\n"
        "\033[1;37mFeature: Dumb feature                    \033[1;30m# tests/functional/output_features/many_successful_scenarios/first.feature:1\033[0m\n"
        "\033[1;37m  In order to test success               \033[1;30m# tests/functional/output_features/many_successful_scenarios/first.feature:2\033[0m\n"
        "\033[1;37m  As a programmer                        \033[1;30m# tests/functional/output_features/many_successful_scenarios/first.feature:3\033[0m\n"
        "\033[1;37m  I want to see that the output is green \033[1;30m# tests/functional/output_features/many_successful_scenarios/first.feature:4\033[0m\n"
        "\n"
        "\033[1;37m  Scenario: Do nothing                   \033[1;30m# tests/functional/output_features/many_successful_scenarios/first.feature:6\033[0m\n"
        "\033[1;30m    Given I do nothing                   \033[1;30m# tests/functional/output_features/many_successful_scenarios/dumb_steps.py:6\033[0m\n"
        "\033[A\033[1;32m    Given I do nothing                   \033[1;30m# tests/functional/output_features/many_successful_scenarios/dumb_steps.py:6\033[0m\n"
        "\n"
        "\033[1;37m  Scenario: Do nothing (again)           \033[1;30m# tests/functional/output_features/many_successful_scenarios/first.feature:9\033[0m\n"
        "\033[1;30m    Given I do nothing (again)           \033[1;30m# tests/functional/output_features/many_successful_scenarios/dumb_steps.py:6\033[0m\n"
        "\033[A\033[1;32m    Given I do nothing (again)           \033[1;30m# tests/functional/output_features/many_successful_scenarios/dumb_steps.py:6\033[0m\n"
        "\n"
        "\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n"
        "\033[1;37m2 scenarios (\033[1;32m2 passed\033[1;37m)\033[0m\n"
        "\033[1;37m2 steps (\033[1;32m2 passed\033[1;37m)\033[0m\n"
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorless_many_features():
    "Testing the output of many successful features"
    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'many_successful_features'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        "\n"
        "Feature: First feature, of many              # tests/functional/output_features/many_successful_features/one.feature:1\n"
        "  In order to make lettuce more robust       # tests/functional/output_features/many_successful_features/one.feature:2\n"
        "  As a programmer                            # tests/functional/output_features/many_successful_features/one.feature:3\n"
        "  I want to test its output on many features # tests/functional/output_features/many_successful_features/one.feature:4\n"
        "\n"
        "  Scenario: Do nothing                       # tests/functional/output_features/many_successful_features/one.feature:6\n"
        "    Given I do nothing                       # tests/functional/output_features/many_successful_features/dumb_steps.py:6\n"
        "    Then I see that the test passes          # tests/functional/output_features/many_successful_features/dumb_steps.py:8\n"
        "\n"
        "Feature: Second feature, of many    # tests/functional/output_features/many_successful_features/two.feature:1\n"
        "  I just want to see it green :)    # tests/functional/output_features/many_successful_features/two.feature:2\n"
        "\n"
        "  Scenario: Do nothing              # tests/functional/output_features/many_successful_features/two.feature:4\n"
        "    Given I do nothing              # tests/functional/output_features/many_successful_features/dumb_steps.py:6\n"
        "    Then I see that the test passes # tests/functional/output_features/many_successful_features/dumb_steps.py:8\n"
        "\n"
        "2 features (2 passed)\n"
        "2 scenarios (2 passed)\n"
        "4 steps (4 passed)\n"
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorful_many_features():
    "Testing the colorful output of many successful features"

    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'many_successful_features'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        "\n"
        "\033[1;37mFeature: First feature, of many              \033[1;30m# tests/functional/output_features/many_successful_features/one.feature:1\033[0m\n"
        "\033[1;37m  In order to make lettuce more robust       \033[1;30m# tests/functional/output_features/many_successful_features/one.feature:2\033[0m\n"
        "\033[1;37m  As a programmer                            \033[1;30m# tests/functional/output_features/many_successful_features/one.feature:3\033[0m\n"
        "\033[1;37m  I want to test its output on many features \033[1;30m# tests/functional/output_features/many_successful_features/one.feature:4\033[0m\n"
        "\n"
        "\033[1;37m  Scenario: Do nothing                       \033[1;30m# tests/functional/output_features/many_successful_features/one.feature:6\033[0m\n"
        "\033[1;30m    Given I do nothing                       \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:6\033[0m\n"
        "\033[A\033[1;32m    Given I do nothing                       \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:6\033[0m\n"
        "\033[1;30m    Then I see that the test passes          \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:8\033[0m\n"
        "\033[A\033[1;32m    Then I see that the test passes          \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:8\033[0m\n"
        "\n"
        "\033[1;37mFeature: Second feature, of many    \033[1;30m# tests/functional/output_features/many_successful_features/two.feature:1\033[0m\n"
        "\033[1;37m  I just want to see it green :)    \033[1;30m# tests/functional/output_features/many_successful_features/two.feature:2\033[0m\n"
        "\n"
        "\033[1;37m  Scenario: Do nothing              \033[1;30m# tests/functional/output_features/many_successful_features/two.feature:4\033[0m\n"
        "\033[1;30m    Given I do nothing              \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:6\033[0m\n"
        "\033[A\033[1;32m    Given I do nothing              \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:6\033[0m\n"
        "\033[1;30m    Then I see that the test passes \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:8\033[0m\n"
        "\033[A\033[1;32m    Then I see that the test passes \033[1;30m# tests/functional/output_features/many_successful_features/dumb_steps.py:8\033[0m\n"
        "\n"
        "\033[1;37m2 features (\033[1;32m2 passed\033[1;37m)\033[0m\n"
        "\033[1;37m2 scenarios (\033[1;32m2 passed\033[1;37m)\033[0m\n"
        "\033[1;37m4 steps (\033[1;32m4 passed\033[1;37m)\033[0m\n"
    )


@with_setup(prepare_stdout)
def test_output_when_could_not_find_features():
    "Testing the colorful output of many successful features"

    path = fs.relpath(join(abspath(dirname(__file__)), 'no_features', 'unexistent-folder'))
    runner = Runner(path, verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        '\033[1;31mOops!\033[0m\n'
        '\033[1;37mcould not find features at \033[1;33m./%s\033[0m\n' % path
    )


@with_setup(prepare_stdout)
def test_output_when_could_not_find_features_colorless():
    "Testing the colorful output of many successful features colorless"

    path = fs.relpath(join(abspath(dirname(__file__)), 'no_features', 'unexistent-folder'))
    runner = Runner(path, verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        'Oops!\n'
        'could not find features at ./%s\n' % path
    )


@with_setup(prepare_stdout)
def test_output_when_could_not_find_features_verbosity_level_2():
    "Testing the colorful output of many successful features colorless"

    path = fs.relpath(join(abspath(dirname(__file__)), 'no_features', 'unexistent-folder'))
    runner = Runner(path, verbosity=2)
    runner.run()

    assert_stdout_lines(
        'Oops!\n'
        'could not find features at ./%s\n' % path
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorless_with_table():
    "Testing the colorless output of success with table"

    runner = Runner(feature_name('success_table'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        '\n'
        'Feature: Table Success           # tests/functional/output_features/success_table/success_table.feature:1\n'
        '\n'
        '  Scenario: Add two numbers ♥    # tests/functional/output_features/success_table/success_table.feature:2\n'
        '    Given I have 0 bucks         # tests/functional/output_features/success_table/success_table_steps.py:28\n'
        '    And that I have these items: # tests/functional/output_features/success_table/success_table_steps.py:32\n'
        '      | name    | price  |\n'
        '      | Porsche | 200000 |\n'
        '      | Ferrari | 400000 |\n'
        '    When I sell the "Ferrari"    # tests/functional/output_features/success_table/success_table_steps.py:42\n'
        '    Then I have 400000 bucks     # tests/functional/output_features/success_table/success_table_steps.py:28\n'
        '    And my garage contains:      # tests/functional/output_features/success_table/success_table_steps.py:47\n'
        '      | name    | price  |\n'
        '      | Porsche | 200000 |\n'
        '\n'
        '1 feature (1 passed)\n'
        '1 scenario (1 passed)\n'
        '5 steps (5 passed)\n'
    )


@with_setup(prepare_stdout)
def test_output_with_success_colorful_with_table():
    "Testing the colorful output of success with table"

    runner = Runner(feature_name('success_table'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        '\n'
        '\033[1;37mFeature: Table Success           \033[1;30m# tests/functional/output_features/success_table/success_table.feature:1\033[0m\n'
        '\n'
        '\033[1;37m  Scenario: Add two numbers ♥    \033[1;30m# tests/functional/output_features/success_table/success_table.feature:2\033[0m\n'
        '\033[1;30m    Given I have 0 bucks         \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:28\033[0m\n'
        '\033[A\033[1;32m    Given I have 0 bucks         \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:28\033[0m\n'
        '\033[1;30m    And that I have these items: \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:32\033[0m\n'
        '\033[1;30m     \033[1;37m |\033[1;30m name   \033[1;37m |\033[1;30m price \033[1;37m |\033[1;30m\033[0m\n'
        '\033[1;30m     \033[1;37m |\033[1;30m Porsche\033[1;37m |\033[1;30m 200000\033[1;37m |\033[1;30m\033[0m\n'
        '\033[1;30m     \033[1;37m |\033[1;30m Ferrari\033[1;37m |\033[1;30m 400000\033[1;37m |\033[1;30m\033[0m\n'
        '\033[A\033[A\033[A\033[A\033[1;32m    And that I have these items: \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:32\033[0m\n'
        '\033[1;32m     \033[1;37m |\033[1;32m name   \033[1;37m |\033[1;32m price \033[1;37m |\033[1;32m\033[0m\n'
        '\033[1;32m     \033[1;37m |\033[1;32m Porsche\033[1;37m |\033[1;32m 200000\033[1;37m |\033[1;32m\033[0m\n'
        '\033[1;32m     \033[1;37m |\033[1;32m Ferrari\033[1;37m |\033[1;32m 400000\033[1;37m |\033[1;32m\033[0m\n'
        '\033[1;30m    When I sell the "Ferrari"    \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:42\033[0m\n'
        '\033[A\033[1;32m    When I sell the "Ferrari"    \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:42\033[0m\n'
        '\033[1;30m    Then I have 400000 bucks     \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:28\033[0m\n'
        '\033[A\033[1;32m    Then I have 400000 bucks     \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:28\033[0m\n'
        '\033[1;30m    And my garage contains:      \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:47\033[0m\n'
        '\033[1;30m     \033[1;37m |\033[1;30m name   \033[1;37m |\033[1;30m price \033[1;37m |\033[1;30m\033[0m\n'
        '\033[1;30m     \033[1;37m |\033[1;30m Porsche\033[1;37m |\033[1;30m 200000\033[1;37m |\033[1;30m\033[0m\n'
        '\033[A\033[A\033[A\033[1;32m    And my garage contains:      \033[1;30m# tests/functional/output_features/success_table/success_table_steps.py:47\033[0m\n'
        '\033[1;32m     \033[1;37m |\033[1;32m name   \033[1;37m |\033[1;32m price \033[1;37m |\033[1;32m\033[0m\n'
        '\033[1;32m     \033[1;37m |\033[1;32m Porsche\033[1;37m |\033[1;32m 200000\033[1;37m |\033[1;32m\033[0m\n'
        '\n'
        "\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 scenario (\033[1;32m1 passed\033[1;37m)\033[0m\n"
        "\033[1;37m5 steps (\033[1;32m5 passed\033[1;37m)\033[0m\n"
    )


@with_setup(prepare_stdout)
def test_output_with_failed_colorless_with_table():
    "Testing the colorless output of failed with table"

    runner = Runner(feature_name('failed_table'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines_with_traceback(
        ("\n"
        "Feature: Table Fail                           # tests/functional/output_features/failed_table/failed_table.feature:1\n"
        "\n"
        "  Scenario: See it fail                       # tests/functional/output_features/failed_table/failed_table.feature:2\n"
        u"    Given I have a dumb step that passes ♥    # tests/functional/output_features/failed_table/failed_table_steps.py:20\n"
        "    And this one fails                        # tests/functional/output_features/failed_table/failed_table_steps.py:24\n"
        "    Traceback (most recent call last):\n"
        '      File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "        ret = self.function(self.step, *args, **kw)\n"
        '      File "%(step_file)s", line 25, in tof\n'
        "        assert False\n"
        "    AssertionError\n"
        "    Then this one will be skipped             # tests/functional/output_features/failed_table/failed_table_steps.py:28\n"
        "    And this one will be skipped              # tests/functional/output_features/failed_table/failed_table_steps.py:28\n"
        "    And this one does not even has definition # tests/functional/output_features/failed_table/failed_table.feature:12 (undefined)\n"
        "\n"
        "1 feature (0 passed)\n"
        "1 scenario (0 passed)\n"
        "5 steps (1 failed, 2 skipped, 1 undefined, 1 passed)\n"
        "\n"
        "You can implement step definitions for undefined steps with these snippets:\n"
        "\n"
        "# -*- coding: utf-8 -*-\n"
        "from lettuce import step\n"
        "\n"
        "@step(u'And this one does not even has definition')\n"
        "def and_this_one_does_not_even_has_definition(step):\n"
        "    assert False, 'This step must be implemented'\n"
        "\n"
        "List of failed scenarios:\n"
        "  Scenario: See it fail                       # tests/functional/output_features/failed_table/failed_table.feature:2\n"
        "\n") % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'failed_table', 'failed_table_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_output_with_failed_colorful_with_table():
    "Testing the colorful output of failed with table"

    runner = Runner(feature_name('failed_table'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines_with_traceback(
        "\n"
        "\033[1;37mFeature: Table Fail                           \033[1;30m# tests/functional/output_features/failed_table/failed_table.feature:1\033[0m\n"
        "\n"
        "\033[1;37m  Scenario: See it fail                       \033[1;30m# tests/functional/output_features/failed_table/failed_table.feature:2\033[0m\n"
        u"\033[1;30m    Given I have a dumb step that passes ♥    \033[1;30m# tests/functional/output_features/failed_table/failed_table_steps.py:20\033[0m\n"
        u"\033[A\033[1;32m    Given I have a dumb step that passes ♥    \033[1;30m# tests/functional/output_features/failed_table/failed_table_steps.py:20\033[0m\n"
        "\033[1;30m    And this one fails                        \033[1;30m# tests/functional/output_features/failed_table/failed_table_steps.py:24\033[0m\n"
        "\033[A\033[0;31m    And this one fails                        \033[1;41;33m# tests/functional/output_features/failed_table/failed_table_steps.py:24\033[0m\n"
        "\033[1;31m    Traceback (most recent call last):\n"
        '      File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "        ret = self.function(self.step, *args, **kw)\n"
        '      File "%(step_file)s", line 25, in tof\n'
        "        assert False\n"
        "    AssertionError\033[0m\n"
        "\033[1;30m    Then this one will be skipped             \033[1;30m# tests/functional/output_features/failed_table/failed_table_steps.py:28\033[0m\n"
        "\033[A\033[0;36m    Then this one will be skipped             \033[1;30m# tests/functional/output_features/failed_table/failed_table_steps.py:28\033[0m\n"
        "\033[1;30m    And this one will be skipped              \033[1;30m# tests/functional/output_features/failed_table/failed_table_steps.py:28\033[0m\n"
        "\033[A\033[0;36m    And this one will be skipped              \033[1;30m# tests/functional/output_features/failed_table/failed_table_steps.py:28\033[0m\n"
        "\033[0;33m    And this one does not even has definition \033[1;30m# tests/functional/output_features/failed_table/failed_table.feature:12\033[0m\n"
        "\n"
        "\033[1;37m1 feature (\033[0;31m0 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 scenario (\033[0;31m0 passed\033[1;37m)\033[0m\n"
        "\033[1;37m5 steps (\033[0;31m1 failed\033[1;37m, \033[0;36m2 skipped\033[1;37m, \033[0;33m1 undefined\033[1;37m, \033[1;32m1 passed\033[1;37m)\033[0m\n"
        "\n"
        "\033[0;33mYou can implement step definitions for undefined steps with these snippets:\n"
        "\n"
        "# -*- coding: utf-8 -*-\n"
        "from lettuce import step\n"
        "\n"
        "@step(u'And this one does not even has definition')\n"
        "def and_this_one_does_not_even_has_definition(step):\n"
        "    assert False, 'This step must be implemented'\033[0m"
        "\n"
        "\n"
        "\033[1;31mList of failed scenarios:\n"
        "\033[0;31m  Scenario: See it fail                       # tests/functional/output_features/failed_table/failed_table.feature:2\n"
        "\033[0m\n" % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'failed_table', 'failed_table_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_output_with_successful_outline_colorless():
    "With colorless output, a successful outline scenario should print beautifully."

    runner = Runner(feature_name('success_outline'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        '\n'
        'Feature: Successful Scenario Outline                          # tests/functional/output_features/success_outline/success_outline.feature:1\n'
        '  As lettuce author                                           # tests/functional/output_features/success_outline/success_outline.feature:2\n'
        '  In order to finish the first release                        # tests/functional/output_features/success_outline/success_outline.feature:3\n'
        u'  I want to make scenario outlines work ♥                     # tests/functional/output_features/success_outline/success_outline.feature:4\n'
        '\n'
        '  Scenario Outline: fill a web form                           # tests/functional/output_features/success_outline/success_outline.feature:6\n'
        '    Given I open browser at "http://www.my-website.com/"      # tests/functional/output_features/success_outline/success_outline_steps.py:21\n'
        '    And click on "sign-up"                                    # tests/functional/output_features/success_outline/success_outline_steps.py:25\n'
        '    When I fill the field "username" with "<username>"        # tests/functional/output_features/success_outline/success_outline_steps.py:29\n'
        '    And I fill the field "password" with "<password>"         # tests/functional/output_features/success_outline/success_outline_steps.py:29\n'
        '    And I fill the field "password-confirm" with "<password>" # tests/functional/output_features/success_outline/success_outline_steps.py:29\n'
        '    And I fill the field "email" with "<email>"               # tests/functional/output_features/success_outline/success_outline_steps.py:29\n'
        '    And I click "done"                                        # tests/functional/output_features/success_outline/success_outline_steps.py:33\n'
        '    Then I see the title of the page is "<title>"             # tests/functional/output_features/success_outline/success_outline_steps.py:37\n'
        '\n'
        '  Examples:\n'
        '    | username | password | email          | title             |\n'
        '    | john     | doe-1234 | john@gmail.org | John \| My Website |\n'
        '    | mary     | wee-9876 | mary@email.com | Mary \| My Website |\n'
        '    | foo      | foo-bar  | foo@bar.com    | Foo \| My Website  |\n'
        '\n'
        '1 feature (1 passed)\n'
        '3 scenarios (3 passed)\n'
        '24 steps (24 passed)\n'
    )


@with_setup(prepare_stdout)
def test_output_with_successful_outline_colorful():
    "With colored output, a successful outline scenario should print beautifully."

    runner = Runner(feature_name('success_outline'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines_with_traceback(
        '\n'
        '\033[1;37mFeature: Successful Scenario Outline                          \033[1;30m# tests/functional/output_features/success_outline/success_outline.feature:1\033[0m\n'
        '\033[1;37m  As lettuce author                                           \033[1;30m# tests/functional/output_features/success_outline/success_outline.feature:2\033[0m\n'
        '\033[1;37m  In order to finish the first release                        \033[1;30m# tests/functional/output_features/success_outline/success_outline.feature:3\033[0m\n'
        u'\033[1;37m  I want to make scenario outlines work ♥                     \033[1;30m# tests/functional/output_features/success_outline/success_outline.feature:4\033[0m\n'
        '\n'
        '\033[1;37m  Scenario Outline: fill a web form                           \033[1;30m# tests/functional/output_features/success_outline/success_outline.feature:6\033[0m\n'
        '\033[0;36m    Given I open browser at "http://www.my-website.com/"      \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:21\033[0m\n'
        '\033[0;36m    And click on "sign-up"                                    \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:25\033[0m\n'
        '\033[0;36m    When I fill the field "username" with "<username>"        \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I fill the field "password" with "<password>"         \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I fill the field "password-confirm" with "<password>" \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I fill the field "email" with "<email>"               \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I click "done"                                        \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:33\033[0m\n'
        '\033[0;36m    Then I see the title of the page is "<title>"             \033[1;30m# tests/functional/output_features/success_outline/success_outline_steps.py:37\033[0m\n'
        '\n'
        '\033[1;37m  Examples:\033[0m\n'
        '\033[0;36m   \033[1;37m |\033[0;36m username\033[1;37m |\033[0;36m password\033[1;37m |\033[0;36m email         \033[1;37m |\033[0;36m title            \033[1;37m |\033[0;36m\033[0m\n'
        '\033[1;32m   \033[1;37m |\033[1;32m john    \033[1;37m |\033[1;32m doe-1234\033[1;37m |\033[1;32m john@gmail.org\033[1;37m |\033[1;32m John \| My Website\033[1;37m |\033[1;32m\033[0m\n'
        '\033[1;32m   \033[1;37m |\033[1;32m mary    \033[1;37m |\033[1;32m wee-9876\033[1;37m |\033[1;32m mary@email.com\033[1;37m |\033[1;32m Mary \| My Website\033[1;37m |\033[1;32m\033[0m\n'
        '\033[1;32m   \033[1;37m |\033[1;32m foo     \033[1;37m |\033[1;32m foo-bar \033[1;37m |\033[1;32m foo@bar.com   \033[1;37m |\033[1;32m Foo \| My Website \033[1;37m |\033[1;32m\033[0m\n'
        '\n'
        "\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n"
        "\033[1;37m3 scenarios (\033[1;32m3 passed\033[1;37m)\033[0m\n"
        "\033[1;37m24 steps (\033[1;32m24 passed\033[1;37m)\033[0m\n"
    )


@with_setup(prepare_stdout)
def test_output_with_failful_outline_colorless():
    "With colorless output, an unsuccessful outline scenario should print beautifully."

    runner = Runner(feature_name('fail_outline'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines_with_traceback(
        '\n'
        'Feature: Failful Scenario Outline                             # tests/functional/output_features/fail_outline/fail_outline.feature:1\n'
        '  As lettuce author                                           # tests/functional/output_features/fail_outline/fail_outline.feature:2\n'
        '  In order to finish the first release                        # tests/functional/output_features/fail_outline/fail_outline.feature:3\n'
        u'  I want to make scenario outlines work ♥                     # tests/functional/output_features/fail_outline/fail_outline.feature:4\n'
        '\n'
        '  Scenario Outline: fill a web form                           # tests/functional/output_features/fail_outline/fail_outline.feature:6\n'
        '    Given I open browser at "http://www.my-website.com/"      # tests/functional/output_features/fail_outline/fail_outline_steps.py:21\n'
        '    And click on "sign-up"                                    # tests/functional/output_features/fail_outline/fail_outline_steps.py:25\n'
        '    When I fill the field "username" with "<username>"        # tests/functional/output_features/fail_outline/fail_outline_steps.py:29\n'
        '    And I fill the field "password" with "<password>"         # tests/functional/output_features/fail_outline/fail_outline_steps.py:29\n'
        '    And I fill the field "password-confirm" with "<password>" # tests/functional/output_features/fail_outline/fail_outline_steps.py:29\n'
        '    And I fill the field "email" with "<email>"               # tests/functional/output_features/fail_outline/fail_outline_steps.py:29\n'
        '    And I click "done"                                        # tests/functional/output_features/fail_outline/fail_outline_steps.py:33\n'
        '    Then I see the message "<message>"                        # tests/functional/output_features/fail_outline/fail_outline_steps.py:37\n'
        '\n'
        '  Examples:\n'
        '    | username | password | email          | message       |\n'
        '    | john     | doe-1234 | john@gmail.org | Welcome, John |\n'
        '    | mary     | wee-9876 | mary@email.com | Welcome, Mary |\n'
        "    Traceback (most recent call last):\n"
        '      File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "        ret = self.function(self.step, *args, **kw)\n"
        '      File "%(step_file)s", line 30, in when_i_fill_the_field_x_with_y\n'
        "        if field == 'password' and value == 'wee-9876':  assert False\n"
        "    AssertionError\n"
        '    | foo      | foo-bar  | foo@bar.com    | Welcome, Foo  |\n'
        '\n'
        '1 feature (0 passed)\n'
        '3 scenarios (2 passed)\n'
        '24 steps (1 failed, 4 skipped, 19 passed)\n'
        '\n'
        'List of failed scenarios:\n'
        '  Scenario Outline: fill a web form                           # tests/functional/output_features/fail_outline/fail_outline.feature:6\n'
        '\n' % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'fail_outline', 'fail_outline_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_output_with_failful_outline_colorful():
    "With colored output, an unsuccessful outline scenario should print beautifully."

    runner = Runner(feature_name('fail_outline'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines_with_traceback(
        '\n'
        '\033[1;37mFeature: Failful Scenario Outline                             \033[1;30m# tests/functional/output_features/fail_outline/fail_outline.feature:1\033[0m\n'
        '\033[1;37m  As lettuce author                                           \033[1;30m# tests/functional/output_features/fail_outline/fail_outline.feature:2\033[0m\n'
        '\033[1;37m  In order to finish the first release                        \033[1;30m# tests/functional/output_features/fail_outline/fail_outline.feature:3\033[0m\n'
        u'\033[1;37m  I want to make scenario outlines work ♥                     \033[1;30m# tests/functional/output_features/fail_outline/fail_outline.feature:4\033[0m\n'
        '\n'
        '\033[1;37m  Scenario Outline: fill a web form                           \033[1;30m# tests/functional/output_features/fail_outline/fail_outline.feature:6\033[0m\n'
        '\033[0;36m    Given I open browser at "http://www.my-website.com/"      \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:21\033[0m\n'
        '\033[0;36m    And click on "sign-up"                                    \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:25\033[0m\n'
        '\033[0;36m    When I fill the field "username" with "<username>"        \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I fill the field "password" with "<password>"         \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I fill the field "password-confirm" with "<password>" \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I fill the field "email" with "<email>"               \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:29\033[0m\n'
        '\033[0;36m    And I click "done"                                        \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:33\033[0m\n'
        '\033[0;36m    Then I see the message "<message>"                        \033[1;30m# tests/functional/output_features/fail_outline/fail_outline_steps.py:37\033[0m\n'
        '\n'
        '\033[1;37m  Examples:\033[0m\n'
        '\033[0;36m   \033[1;37m |\033[0;36m username\033[1;37m |\033[0;36m password\033[1;37m |\033[0;36m email         \033[1;37m |\033[0;36m message      \033[1;37m |\033[0;36m\033[0m\n'
        '\033[1;32m   \033[1;37m |\033[1;32m john    \033[1;37m |\033[1;32m doe-1234\033[1;37m |\033[1;32m john@gmail.org\033[1;37m |\033[1;32m Welcome, John\033[1;37m |\033[1;32m\033[0m\n'
        '\033[1;31m   \033[1;37m |\033[0;31m mary    \033[1;37m |\033[0;31m wee-9876\033[1;37m |\033[0;31m mary@email.com\033[1;37m |\033[0;31m Welcome, Mary\033[1;37m |\033[0;31m\033[0m\n'
        "\033[1;31m    Traceback (most recent call last):\n"
        '      File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "        ret = self.function(self.step, *args, **kw)\n"
        '      File "%(step_file)s", line 30, in when_i_fill_the_field_x_with_y\n'
        "        if field == 'password' and value == 'wee-9876':  assert False\n"
        "    AssertionError\033[0m\n"
        '\033[1;32m   \033[1;37m |\033[1;32m foo     \033[1;37m |\033[1;32m foo-bar \033[1;37m |\033[1;32m foo@bar.com   \033[1;37m |\033[1;32m Welcome, Foo \033[1;37m |\033[1;32m\033[0m\n'
        '\n'
        "\033[1;37m1 feature (\033[0;31m0 passed\033[1;37m)\033[0m\n"
        "\033[1;37m3 scenarios (\033[1;32m2 passed\033[1;37m)\033[0m\n"
        "\033[1;37m24 steps (\033[0;31m1 failed\033[1;37m, \033[0;36m4 skipped\033[1;37m, \033[1;32m19 passed\033[1;37m)\033[0m\n"
        "\n"
        "\033[1;31mList of failed scenarios:\n"
        "\033[0;31m  Scenario Outline: fill a web form                           # tests/functional/output_features/fail_outline/fail_outline.feature:6\n"
        "\033[0m\n" % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'fail_outline', 'fail_outline_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_output_snippets_with_groups_within_double_quotes_colorless():
    "Testing that the proposed snippet is clever enough to identify groups within double quotes. colorless"

    runner = Runner(feature_name('double-quoted-snippet'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'Feature: double-quoted snippet proposal                          # tests/functional/output_features/double-quoted-snippet/double-quoted-snippet.feature:1\n'
        u'\n'
        u'  Scenario: Propose matched groups                               # tests/functional/output_features/double-quoted-snippet/double-quoted-snippet.feature:2\n'
        u'    Given I have "stuff here" and "more @#$%ˆ& bizar sutff h3r3" # tests/functional/output_features/double-quoted-snippet/double-quoted-snippet.feature:3 (undefined)\n'
        u'\n'
        u'1 feature (0 passed)\n'
        u'1 scenario (0 passed)\n'
        u'1 step (1 undefined, 0 passed)\n'
        u'\n'
        u'You can implement step definitions for undefined steps with these snippets:\n'
        u'\n'
        u"# -*- coding: utf-8 -*-\n"
        u'from lettuce import step\n'
        u'\n'
        u'@step(u\'Given I have "([^\"]*)" and "([^\"]*)"\')\n'
        u'def given_i_have_group1_and_group2(step, group1, group2):\n'
        u'    assert False, \'This step must be implemented\'\n'
    )


@with_setup(prepare_stdout)
def test_output_snippets_with_groups_within_double_quotes_colorful():
    "Testing that the proposed snippet is clever enough to identify groups within double quotes. colorful"

    runner = Runner(feature_name('double-quoted-snippet'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'\033[1;37mFeature: double-quoted snippet proposal                          \033[1;30m# tests/functional/output_features/double-quoted-snippet/double-quoted-snippet.feature:1\033[0m\n'
        u'\n'
        u'\033[1;37m  Scenario: Propose matched groups                               \033[1;30m# tests/functional/output_features/double-quoted-snippet/double-quoted-snippet.feature:2\033[0m\n'
        u'\033[0;33m    Given I have "stuff here" and "more @#$%ˆ& bizar sutff h3r3" \033[1;30m# tests/functional/output_features/double-quoted-snippet/double-quoted-snippet.feature:3\033[0m\n'
        u'\n'
        "\033[1;37m1 feature (\033[0;31m0 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 scenario (\033[0;31m0 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 step (\033[0;33m1 undefined\033[1;37m, \033[1;32m0 passed\033[1;37m)\033[0m\n"
        u'\n'
        u'\033[0;33mYou can implement step definitions for undefined steps with these snippets:\n'
        u'\n'
        u"# -*- coding: utf-8 -*-\n"
        u'from lettuce import step\n'
        u'\n'
        u'@step(u\'Given I have "([^"]*)" and "([^"]*)"\')\n'
        u'def given_i_have_group1_and_group2(step, group1, group2):\n'
        u'    assert False, \'This step must be implemented\'\033[0m\n'
    )


@with_setup(prepare_stdout)
def test_output_snippets_with_groups_within_single_quotes_colorless():
    "Testing that the proposed snippet is clever enough to identify groups within single quotes. colorless"

    runner = Runner(feature_name('single-quoted-snippet'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'Feature: single-quoted snippet proposal                          # tests/functional/output_features/single-quoted-snippet/single-quoted-snippet.feature:1\n'
        u'\n'
        u'  Scenario: Propose matched groups                               # tests/functional/output_features/single-quoted-snippet/single-quoted-snippet.feature:2\n'
        u'    Given I have \'stuff here\' and \'more @#$%ˆ& bizar sutff h3r3\' # tests/functional/output_features/single-quoted-snippet/single-quoted-snippet.feature:3 (undefined)\n'
        u'\n'
        u'1 feature (0 passed)\n'
        u'1 scenario (0 passed)\n'
        u'1 step (1 undefined, 0 passed)\n'
        u'\n'
        u'You can implement step definitions for undefined steps with these snippets:\n'
        u'\n'
        u"# -*- coding: utf-8 -*-\n"
        u'from lettuce import step\n'
        u'\n'
        u'@step(u\'Given I have \\\'([^\\\']*)\\\' and \\\'([^\\\']*)\\\'\')\n'
        u'def given_i_have_group1_and_group2(step, group1, group2):\n'
        u'    assert False, \'This step must be implemented\'\n'
    )


@with_setup(prepare_stdout)
def test_output_snippets_with_groups_within_single_quotes_colorful():
    "Testing that the proposed snippet is clever enough to identify groups within single quotes. colorful"

    runner = Runner(feature_name('single-quoted-snippet'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'\033[1;37mFeature: single-quoted snippet proposal                          \033[1;30m# tests/functional/output_features/single-quoted-snippet/single-quoted-snippet.feature:1\033[0m\n'
        u'\n'
        u'\033[1;37m  Scenario: Propose matched groups                               \033[1;30m# tests/functional/output_features/single-quoted-snippet/single-quoted-snippet.feature:2\033[0m\n'
        u'\033[0;33m    Given I have \'stuff here\' and \'more @#$%ˆ& bizar sutff h3r3\' \033[1;30m# tests/functional/output_features/single-quoted-snippet/single-quoted-snippet.feature:3\033[0m\n'
        u'\n'
        "\033[1;37m1 feature (\033[0;31m0 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 scenario (\033[0;31m0 passed\033[1;37m)\033[0m\n"
        "\033[1;37m1 step (\033[0;33m1 undefined\033[1;37m, \033[1;32m0 passed\033[1;37m)\033[0m\n"
        u'\n'
        u'\033[0;33mYou can implement step definitions for undefined steps with these snippets:\n'
        u'\n'
        u"# -*- coding: utf-8 -*-\n"
        u'from lettuce import step\n'
        u'\n'
        u'@step(u\'Given I have \\\'([^\\\']*)\\\' and \\\'([^\\\']*)\\\'\')\n'
        u'def given_i_have_group1_and_group2(step, group1, group2):\n'
        u'    assert False, \'This step must be implemented\'\033[0m\n'
    )


@with_setup(prepare_stdout)
def test_output_snippets_with_groups_within_redundant_quotes():
    "Testing that the proposed snippet is clever enough to avoid duplicating the same snippet"

    runner = Runner(feature_name('redundant-steps-quotes'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'Feature: avoid duplicating same snippet                          # tests/functional/output_features/redundant-steps-quotes/redundant-steps-quotes.feature:1\n'
        u'\n'
        u'  Scenario: Propose matched groups                               # tests/functional/output_features/redundant-steps-quotes/redundant-steps-quotes.feature:2\n'
        u'    Given I have "stuff here" and "more @#$%ˆ& bizar sutff h3r3" # tests/functional/output_features/redundant-steps-quotes/redundant-steps-quotes.feature:3 (undefined)\n'
        u'    Given I have "blablabla" and "12345"                         # tests/functional/output_features/redundant-steps-quotes/redundant-steps-quotes.feature:4 (undefined)\n'
        u'\n'
        u'1 feature (0 passed)\n'
        u'1 scenario (0 passed)\n'
        u'2 steps (2 undefined, 0 passed)\n'
        u'\n'
        u'You can implement step definitions for undefined steps with these snippets:\n'
        u'\n'
        u"# -*- coding: utf-8 -*-\n"
        u'from lettuce import step\n'
        u'\n'
        u'@step(u\'Given I have "([^"]*)" and "([^"]*)"\')\n'
        u'def given_i_have_group1_and_group2(step, group1, group2):\n'
        u'    assert False, \'This step must be implemented\'\n'
    )


@with_setup(prepare_stdout)
def test_output_snippets_with_normalized_unicode_names():
    "Testing that the proposed snippet is clever enough normalize method names even with latin accents"

    runner = Runner(feature_name('latin-accents'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u"\n"
        u"Funcionalidade: melhorar o output de snippets do lettuce                                      # tests/functional/output_features/latin-accents/latin-accents.feature:2\n"
        u"  Como autor do lettuce                                                                       # tests/functional/output_features/latin-accents/latin-accents.feature:3\n"
        u"  Eu quero ter um output refinado de snippets                                                 # tests/functional/output_features/latin-accents/latin-accents.feature:4\n"
        u"  Para melhorar, de uma forma geral, a vida do programador                                    # tests/functional/output_features/latin-accents/latin-accents.feature:5\n"
        u"\n"
        u"  Cenário: normalizar snippets com unicode                                                    # tests/functional/output_features/latin-accents/latin-accents.feature:7\n"
        u"    Dado que eu tenho palavrões e outras situações                                            # tests/functional/output_features/latin-accents/latin-accents.feature:8 (undefined)\n"
        u"    E várias palavras acentuadas são úteis, tais como: \"(é,não,léo,chororó,chácara,epígrafo)\" # tests/functional/output_features/latin-accents/latin-accents.feature:9 (undefined)\n"
        u"    Então eu fico felizão                                                                     # tests/functional/output_features/latin-accents/latin-accents.feature:10 (undefined)\n"
        u"\n"
        u"1 feature (0 passed)\n"
        u"1 scenario (0 passed)\n"
        u"3 steps (3 undefined, 0 passed)\n"
        u"\n"
        u"You can implement step definitions for undefined steps with these snippets:\n"
        u"\n"
        u"# -*- coding: utf-8 -*-\n"
        u"from lettuce import step\n"
        u"\n"
        u"@step(u'Dado que eu tenho palavrões e outras situações')\n"
        u"def dado_que_eu_tenho_palavroes_e_outras_situacoes(step):\n"
        u"    assert False, 'This step must be implemented'\n"
        u"@step(u'E várias palavras acentuadas são úteis, tais como: \"([^\"]*)\"')\n"
        u"def e_varias_palavras_acentuadas_sao_uteis_tais_como_group1(step, group1):\n"
        u"    assert False, 'This step must be implemented'\n"
        u"@step(u'Então eu fico felizão')\n"
        u"def entao_eu_fico_felizao(step):\n"
        u"    assert False, 'This step must be implemented'\n"
    )


@with_setup(prepare_stdout)
def test_output_level_2_success():
    'Output with verbosity 2 must show only the scenario names, followed by "... OK" in case of success'

    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'many_successful_scenarios'), verbosity=2)
    runner.run()

    assert_stdout_lines(
        "Do nothing ... OK\n"
        "Do nothing (again) ... OK\n"
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "2 steps (2 passed)\n"
    )


@with_setup(prepare_stdout)
def test_output_level_2_fail():
    'Output with verbosity 2 must show only the scenario names, followed by "... FAILED" in case of fail'

    runner = Runner(feature_name('failed_table'), verbosity=2)
    runner.run()

    assert_stdout_lines_with_traceback(
        "See it fail ... FAILED\n"
        "\n"
        "\n"
        "<Step: \"And this one fails\">\n"
        "Traceback (most recent call last):\n"
        '  File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "    ret = self.function(self.step, *args, **kw)\n"
        '  File "%(step_file)s", line 25, in tof\n'
        "    assert False\n"
        "AssertionError\n"
        "\n"
        "1 feature (0 passed)\n"
        "1 scenario (0 passed)\n"
        "5 steps (1 failed, 2 skipped, 1 undefined, 1 passed)\n"
        "\n"
        "List of failed scenarios:\n"
        "  Scenario: See it fail                       # tests/functional/output_features/failed_table/failed_table.feature:2\n"
        "\n" % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'failed_table', 'failed_table_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_output_level_2_error():
    'Output with verbosity 2 must show only the scenario names, followed by "... ERROR" in case of fail'

    runner = Runner(feature_name('error_traceback'), verbosity=2)
    runner.run()

    assert_stdout_lines_with_traceback(
        "It should pass ... OK\n"
        "It should raise an exception different of AssertionError ... ERROR\n"
        "\n"
        "\n"
        "<Step: \"Given my step that blows a exception\">\n"
        "Traceback (most recent call last):\n"
        '  File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "    ret = self.function(self.step, *args, **kw)\n"
        '  File "%(step_file)s", line 10, in given_my_step_that_blows_a_exception\n'
        "    raise RuntimeError\n"
        "RuntimeError\n"
        "\n"
        "1 feature (0 passed)\n"
        "2 scenarios (1 passed)\n"
        "2 steps (1 failed, 1 passed)\n"
        "\n"
        "List of failed scenarios:\n"
        "  Scenario: It should raise an exception different of AssertionError # tests/functional/output_features/error_traceback/error_traceback.feature:5\n"
        "\n" % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'error_traceback', 'error_traceback_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_output_level_1_success():
    'Output with verbosity 2 must show only the scenario names, followed by "... OK" in case of success'

    runner = Runner(join(abspath(dirname(__file__)), 'output_features', 'many_successful_scenarios'), verbosity=1)
    runner.run()

    assert_stdout_lines(
        ".."
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "2 steps (2 passed)\n"
    )


@with_setup(prepare_stdout)
def test_output_level_1_fail():
    'Output with verbosity 2 must show only the scenario names, followed by "... FAILED" in case of fail'

    runner = Runner(feature_name('failed_table'), verbosity=1)
    runner.run()

    assert_stdout_lines_with_traceback(
        "F\n"
        "\n"
        "<Step: \"And this one fails\">\n"
        "Traceback (most recent call last):\n"
        '  File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "    ret = self.function(self.step, *args, **kw)\n"
        '  File "%(step_file)s", line 25, in tof\n'
        "    assert False\n"
        "AssertionError\n"
        "\n"
        "1 feature (0 passed)\n"
        "1 scenario (0 passed)\n"
        "5 steps (1 failed, 2 skipped, 1 undefined, 1 passed)\n"
        "\n"
        "List of failed scenarios:\n"
        "  Scenario: See it fail                       # tests/functional/output_features/failed_table/failed_table.feature:2\n"
        "\n" % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'failed_table', 'failed_table_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_output_level_1_error():
    'Output with verbosity 2 must show only the scenario names, followed by "... ERROR" in case of fail'

    runner = Runner(feature_name('error_traceback'), verbosity=1)
    runner.run()

    assert_stdout_lines_with_traceback(
        ".E\n"
        "\n"
        "<Step: \"Given my step that blows a exception\">\n"
        "Traceback (most recent call last):\n"
        '  File "%(lettuce_core_file)s", line %(call_line)d, in __call__\n'
        "    ret = self.function(self.step, *args, **kw)\n"
        '  File "%(step_file)s", line 10, in given_my_step_that_blows_a_exception\n'
        "    raise RuntimeError\n"
        "RuntimeError\n"
        "\n"
        "1 feature (0 passed)\n"
        "2 scenarios (1 passed)\n"
        "2 steps (1 failed, 1 passed)\n"
        "\n"
        "List of failed scenarios:\n"
        "  Scenario: It should raise an exception different of AssertionError # tests/functional/output_features/error_traceback/error_traceback.feature:5\n"
        "\n" % {
            'lettuce_core_file': lettuce_path('core.py'),
            'step_file': abspath(lettuce_path('..', 'tests', 'functional', 'output_features', 'error_traceback', 'error_traceback_steps.py')),
            'call_line': call_line,
        }
    )


@with_setup(prepare_stdout)
def test_commented_scenario():
    'Test one commented scenario'

    runner = Runner(feature_name('commented_feature'), verbosity=1)
    runner.run()

    assert_stdout_lines(
        "."
        "\n"
        "1 feature (1 passed)\n"
        "1 scenario (1 passed)\n"
        "1 step (1 passed)\n"
    )


@with_setup(prepare_stdout)
def test_blank_step_hash_value():
    "syntax checking: Blank in step hash column = empty string"

    from lettuce import step

    @step('ignore step')
    def ignore_step(step):
        pass

    @step('string length calc')
    def string_lenth_calc(step):
        for hash in step.hashes:
            if len(hash["string"]) + len(hash["string2"]) != int(hash["length"]):
                raise AssertionError("fail")

    filename = syntax_feature_name('blank_values_in_hash')
    runner = Runner(filename, verbosity=1)
    runner.run()

    assert_stdout_lines(
        "."
        "\n"
        "1 feature (1 passed)\n"
        "1 scenario (1 passed)\n"
        "4 steps (4 passed)\n"
    )


@with_setup(prepare_stdout)
def test_run_only_fast_tests():
    "Runner can filter by tags"

    from lettuce import step

    good_one = Mock()
    bad_one = Mock()

    @step('I wait for 0 seconds')
    def wait_for_0_seconds(step):
        good_one(step.sentence)

    @step('the time passed is 0 seconds')
    def time_passed_0_sec(step):
        good_one(step.sentence)

    @step('I wait for 60 seconds')
    def wait_for_60_seconds(step):
        bad_one(step.sentence)

    @step('the time passed is 1 minute')
    def time_passed_1_min(step):
        bad_one(step.sentence)

    filename = tag_feature_name('timebound')
    runner = Runner(filename, verbosity=1, tags=['fast-ish'])
    runner.run()

    assert_stdout_lines(
        "."
        "\n"
        "1 feature (1 passed)\n"
        "1 scenario (1 passed)\n"
        "2 steps (2 passed)\n"
    )


def test_run_random():
    "Randomise the feature order"

    path = fs.relpath(join(abspath(dirname(__file__)), 'no_features', 'unexistent-folder'))

    runner = Runner(path, random=True)
    assert_equals(True, runner.random)
    with patch.object(random, 'shuffle') as pshuffle:
        runner.run()
        pshuffle.assert_called_once_with([])


@with_setup(prepare_stdout)
def test_background_with_header():
    "Running background with header"

    from lettuce import step, world

    @step(ur'the variable "(\w+)" holds (\d+)')
    def set_variable(step, name, value):
        setattr(world, name, int(value))

    @step(ur'the variable "(\w+)" is equal to (\d+)')
    def check_variable(step, name, expected):
        expected = int(expected)
        expect(world).to.have.property(name).being.equal(expected)

    @step(ur'the variable "(\w+)" times (\d+) is equal to (\d+)')
    def multiply_and_verify(step, name, times, expected):
        times = int(times)
        expected = int(expected)
        (getattr(world, name) * times).should.equal(expected)

    filename = bg_feature_name('header')
    runner = Runner(filename, verbosity=1)
    runner.run()

    assert_stdout_lines(
        ".."
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "7 steps (7 passed)\n"
    )


@with_setup(prepare_stdout)
def test_background_without_header():
    "Running background without header"

    from lettuce import step, world, before, after

    actions = {}

    @before.each_background
    def register_background_before(background):
        actions['before'] = unicode(background)

    @after.each_background
    def register_background_after(background, results):
        actions['after'] = {
            'background': unicode(background),
            'results': results,
        }

    @step(ur'the variable "(\w+)" holds (\d+)')
    def set_variable(step, name, value):
        setattr(world, name, int(value))

    @step(ur'the variable "(\w+)" is equal to (\d+)')
    def check_variable(step, name, expected):
        expected = int(expected)
        expect(world).to.have.property(name).being.equal(expected)

    @step(ur'the variable "(\w+)" times (\d+) is equal to (\d+)')
    def multiply_and_verify(step, name, times, expected):
        times = int(times)
        expected = int(expected)
        (getattr(world, name) * times).should.equal(expected)

    filename = bg_feature_name('naked')
    runner = Runner(filename, verbosity=1)
    runner.run()

    assert_stdout_lines(
        ".."
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "7 steps (7 passed)\n"
    )

    expect(actions).to.equal({
        'after': {
            'results': [True],
            'background': u'<Background for feature: Without Header>'
        },
        'before': u'<Background for feature: Without Header>'
    })


@with_setup(prepare_stdout)
def test_output_background_with_success_colorless():
    "A feature with background should print it accordingly under verbosity 3"

    from lettuce import step

    line = currentframe().f_lineno  # get line number
    @step(ur'the variable "(\w+)" holds (\d+)')
    @step(ur'the variable "(\w+)" is equal to (\d+)')
    def just_pass(step, *args):
        pass

    filename = bg_feature_name('simple')
    runner = Runner(filename, verbosity=3, no_color=True)

    runner.run()

    assert_stdout_lines(
        '\n'
        'Feature: Simple and successful                # tests/functional/bg_features/simple/simple.feature:1\n'
        '  As the Lettuce maintainer                   # tests/functional/bg_features/simple/simple.feature:2\n'
        '  In order to make sure the output is pretty  # tests/functional/bg_features/simple/simple.feature:3\n'
        '  I want to automate its test                 # tests/functional/bg_features/simple/simple.feature:4\n'
        '\n'
        '  Background:\n'
        '    Given the variable "X" holds 2            # tests/functional/test_runner.py:{line}\n'
        '\n'
        '  Scenario: multiplication changing the value # tests/functional/bg_features/simple/simple.feature:9\n'
        '    Given the variable "X" is equal to 2      # tests/functional/test_runner.py:{line}\n'
        '\n'
        '1 feature (1 passed)\n'
        '1 scenario (1 passed)\n'
        '1 step (1 passed)\n'
        .format(line=line+2)  # increment is line number of step past line
    )


@with_setup(prepare_stdout)
def test_output_background_with_success_colorful():
    "A feature with background should print it accordingly under verbosity 3 and colored output"

    from lettuce import step

    line = currentframe().f_lineno  # get line number
    @step(ur'the variable "(\w+)" holds (\d+)')
    @step(ur'the variable "(\w+)" is equal to (\d+)')
    def just_pass(step, *args):
        pass

    filename = bg_feature_name('simple')
    runner = Runner(filename, verbosity=3, no_color=False)

    runner.run()

    assert_stdout_lines(
        '\n'
        '\033[1;37mFeature: Simple and successful                \033[1;30m# tests/functional/bg_features/simple/simple.feature:1\033[0m\n'
        '\033[1;37m  As the Lettuce maintainer                   \033[1;30m# tests/functional/bg_features/simple/simple.feature:2\033[0m\n'
        '\033[1;37m  In order to make sure the output is pretty  \033[1;30m# tests/functional/bg_features/simple/simple.feature:3\033[0m\n'
        '\033[1;37m  I want to automate its test                 \033[1;30m# tests/functional/bg_features/simple/simple.feature:4\033[0m\n'
        '\n'
        '\033[1;37m  Background:\033[0m\n'
        '\033[1;30m    Given the variable "X" holds 2            \033[1;30m# tests/functional/test_runner.py:{line}\033[0m\n'
        '\033[A\033[1;32m    Given the variable "X" holds 2            \033[1;30m# tests/functional/test_runner.py:{line}\033[0m\n'
        '\n'
        '\033[1;37m  Scenario: multiplication changing the value \033[1;30m# tests/functional/bg_features/simple/simple.feature:9\033[0m\n'
        '\033[1;30m    Given the variable "X" is equal to 2      \033[1;30m# tests/functional/test_runner.py:{line}\033[0m\n'
        '\033[A\033[1;32m    Given the variable "X" is equal to 2      \033[1;30m# tests/functional/test_runner.py:{line}\033[0m\n'
        '\n'
        '\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n'
        '\033[1;37m1 scenario (\033[1;32m1 passed\033[1;37m)\033[0m\n'
        '\033[1;37m1 step (\033[1;32m1 passed\033[1;37m)\033[0m\n'
        .format(line=line+2)  # increment is line number of step past line
    )


@with_setup(prepare_stdout)
def test_background_with_scenario_before_hook():
    "Running background with before_scenario hook"

    from lettuce import step, world, before

    @before.each_scenario
    def reset_variable(scenario):
        world.X = None

    @step(ur'the variable "(\w+)" holds (\d+)')
    def set_variable(step, name, value):
        setattr(world, name, int(value))

    @step(ur'the variable "(\w+)" is equal to (\d+)')
    def check_variable(step, name, expected):
        expected = int(expected)
        expect(world).to.have.property(name).being.equal(expected)

    @step(ur'the variable "(\w+)" times (\d+) is equal to (\d+)')
    def multiply_and_verify(step, name, times, expected):
        times = int(times)
        expected = int(expected)
        (getattr(world, name) * times).should.equal(expected)

    filename = bg_feature_name('header')
    runner = Runner(filename, verbosity=1)
    runner.run()

    assert_stdout_lines(
        ".."
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "7 steps (7 passed)\n"
    )


@with_setup(prepare_stderr)
def test_many_features_a_file():
    "syntax checking: Fail if a file has more than one feature"

    filename = syntax_feature_name('many_features_a_file')
    runner = Runner(filename)
    assert_raises(SystemExit, runner.run)

    assert_stderr_lines(
        'Syntax error at: %s\n'
        'A feature file must contain ONLY ONE feature!\n' % filename
    )


@with_setup(prepare_stderr)
def test_feature_without_name():
    "syntax checking: Fail on features without name"

    filename = syntax_feature_name('feature_without_name')
    runner = Runner(filename)

    assert_raises(SystemExit, runner.run)

    assert_stderr_lines(
        'Syntax error at: %s\n'
        'Features must have a name. e.g: "Feature: This is my name"\n'
        % filename
    )


@with_setup(prepare_stderr)
def test_feature_missing_scenarios():
    "syntax checking: Fail on features missing scenarios"

    filename = syntax_feature_name("feature_missing_scenarios")
    runner = Runner(filename)

    assert_raises(SystemExit, runner.run)

    assert_stderr_lines(
        u"Syntax error at: %s\n"
        "Features must have scenarios.\nPlease refer to the documentation "
        "available at http://lettuce.it for more information.\n" % filename
    )

@with_setup(prepare_stdout)
def test_output_with_undefined_steps_colorful():
    "With colored output, an undefined step should be printed in sequence."

    runner = Runner(feature_name('undefined_steps'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines_with_traceback(
        '\n'
        '\x1b[1;37mFeature: Test undefined steps are displayed on console           \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.feature:1\x1b[0m\n'
        '\n'
        '\x1b[1;37m  Scenario: Scenario with undefined step                         \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.feature:3\x1b[0m\n'
        '\x1b[1;30m    Given this test step passes                                  \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.py:4\x1b[0m\n'
        '\x1b[A\x1b[1;32m    Given this test step passes                                  \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.py:4\x1b[0m\n'
        '\x1b[0;33m    When this test step is undefined                             \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.feature:5\x1b[0m\n'
        '\n'
        '\x1b[1;37m  Scenario Outline: Outline scenario with general undefined step \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.feature:7\x1b[0m\n'
        '\x1b[0;36m    Given this test step passes                                  \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.py:4\x1b[0m\n'
        '\x1b[0;33m    When this test step is undefined                             \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.feature:5\x1b[0m\n'
        '\x1b[0;36m    Then <in> squared is <out>                                   \x1b[1;30m# tests/functional/output_features/undefined_steps/undefined_steps.py:8\x1b[0m\n'
        '\n'
        '\x1b[1;37m  Examples:\x1b[0m\n'
        '\x1b[0;36m   \x1b[1;37m |\x1b[0;36m in\x1b[1;37m |\x1b[0;36m out\x1b[1;37m |\x1b[0;36m\x1b[0m\n'
        '\x1b[1;32m   \x1b[1;37m |\x1b[1;32m 1 \x1b[1;37m |\x1b[1;32m 1  \x1b[1;37m |\x1b[1;32m\x1b[0m\n'
        '\x1b[1;32m   \x1b[1;37m |\x1b[1;32m 2 \x1b[1;37m |\x1b[1;32m 4  \x1b[1;37m |\x1b[1;32m\x1b[0m\n'
        '\n'
        '\x1b[1;37m1 feature (\x1b[0;31m0 passed\x1b[1;37m)\x1b[0m\n'
        '\x1b[1;37m3 scenarios (\x1b[0;31m0 passed\x1b[1;37m)\x1b[0m\n'
        '\x1b[1;37m8 steps (\x1b[0;36m2 skipped\x1b[1;37m, \x1b[0;33m3 undefined\x1b[1;37m, \x1b[1;32m3 passed\x1b[1;37m)\x1b[0m\n'
        '\n'
        '\x1b[0;33mYou can implement step definitions for undefined steps with these snippets:\n'
        '\n'
        '# -*- coding: utf-8 -*-\n'
        'from lettuce import step\n'
        '\n'
        "@step(u'When this test step is undefined')\n"
        'def when_this_test_step_is_undefined(step):\n'
        "    assert False, 'This step must be implemented'\x1b[0m\n"
    )

