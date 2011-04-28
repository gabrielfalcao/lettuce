# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2011>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from nose.tools import with_setup
from os.path import dirname, join, abspath

from lettuce import Runner

from tests.asserts import prepare_stdout
from tests.asserts import assert_stdout_lines
from tests.asserts import assert_stdout_lines_with_traceback

def path_to_feature(name):
    return join(abspath(dirname(__file__)), 'behave_as_features', name, "%s.feature" % name)

@with_setup(prepare_stdout)
def test_simple_behave_as_feature():
    "Basic step.behave_as behaviour is working"
    Runner(path_to_feature('1st_normal_steps'), verbosity=3).run()
    assert_stdout_lines(
        "\n"
        "Feature: Multiplication                            # tests/functional/behave_as_features/1st_normal_steps/1st_normal_steps.feature:2\n"
        "  In order to avoid silly mistakes                 # tests/functional/behave_as_features/1st_normal_steps/1st_normal_steps.feature:3\n"
        "  Cashiers must be able to multiplicate numbers :) # tests/functional/behave_as_features/1st_normal_steps/1st_normal_steps.feature:4\n"
        "\n"
        "  Scenario: Regular numbers                        # tests/functional/behave_as_features/1st_normal_steps/1st_normal_steps.feature:6\n"
        "    Given I have entered 10 into the calculator    # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:11\n"
        "\033[A    Given I have entered 10 into the calculator    # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:11\n"
        "    And I have entered 4 into the calculator       # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:11\n"
        "\033[A    And I have entered 4 into the calculator       # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:11\n"
        "    When I press multiply                          # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:15\n"
        "\033[A    When I press multiply                          # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:15\n"
        "    Then the result should be 40 on the screen     # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:19\n"
        "\033[A    Then the result should be 40 on the screen     # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:19\n"
        "\n"
        "  Scenario: Shorter version of the scenario above  # tests/functional/behave_as_features/1st_normal_steps/1st_normal_steps.feature:12\n"
        "    Given I multiply 10 and 4 into the calculator  # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:23\n"
        "\033[A    Given I multiply 10 and 4 into the calculator  # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:23\n"
        "    Then the result should be 40 on the screen     # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:19\n"
        "\033[A    Then the result should be 40 on the screen     # tests/functional/behave_as_features/1st_normal_steps/simple_step_definitions.py:19\n"
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "6 steps (6 passed)\n"
    )

@with_setup(prepare_stdout)
def test_simple_tables_behave_as_feature():
    "Basic step.behave_as behaviour is working"
    Runner(path_to_feature('2nd_table_steps'), verbosity=3).run()
    assert_stdout_lines(
        "\n"
        "Feature: Multiplication                            # tests/functional/behave_as_features/2nd_table_steps/2nd_table_steps.feature:2\n"
        "  In order to avoid silly mistakes                 # tests/functional/behave_as_features/2nd_table_steps/2nd_table_steps.feature:3\n"
        "  Cashiers must be able to multiplicate numbers :) # tests/functional/behave_as_features/2nd_table_steps/2nd_table_steps.feature:4\n"
        "\n"
        "  Scenario: Regular numbers                        # tests/functional/behave_as_features/2nd_table_steps/2nd_table_steps.feature:6\n"
        "    Given I have entered 10 into the calculator    # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:11\n"
        "\033[A    Given I have entered 10 into the calculator    # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:11\n"
        "    And I have entered 4 into the calculator       # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:11\n"
        "\033[A    And I have entered 4 into the calculator       # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:11\n"
        "    When I press multiply                          # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:15\n"
        "\033[A    When I press multiply                          # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:15\n"
        "    Then the result should be 40 on the screen     # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:19\n"
        "\033[A    Then the result should be 40 on the screen     # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:19\n"
        "\n"
        "  Scenario: Shorter version of the scenario above  # tests/functional/behave_as_features/2nd_table_steps/2nd_table_steps.feature:12\n"
        "    Given I multiply 10 and 4 into the calculator  # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:23\n"
        "\033[A    Given I multiply 10 and 4 into the calculator  # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:23\n"
        "    Then the result should be 40 on the screen     # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:19\n"
        "\033[A    Then the result should be 40 on the screen     # tests/functional/behave_as_features/2nd_table_steps/simple_tables_step_definitions.py:19\n"
        "\n"
        "1 feature (1 passed)\n"
        "2 scenarios (2 passed)\n"
        "6 steps (6 passed)\n"
    )

