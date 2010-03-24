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

SCENARIO1 = """
Scenario: Adding some students to my university database
    Given I have the following courses in my university:
       | Name               | Duration |
       | Computer Science   | 5 years  |
       | Nutrition          | 4 years  |
    When I consolidate the database into 'courses.txt'
    Then I see the 1st line of 'courses.txt' has 'Computer Science:5'
    And I see the 2nd line of 'courses.txt' has 'Nutrition:4'
"""

from lettuce.core import Step
from lettuce.core import Scenario
from nose.tools import assert_equals

def test_scenario_has_name():
    "It should extract the name of the scenario"

    scenario = Scenario.from_string(SCENARIO1)

    assert isinstance(scenario, Scenario)

    assert_equals(
        scenario.name,
        "Adding some students to my university database"
    )

def test_scenario_has_steps():
    "A scenario object should have a list of steps"

    scenario = Scenario.from_string(SCENARIO1)

    assert_equals(type(scenario.steps), list)
    assert_equals(len(scenario.steps), 4, "It should have 4 steps")

    expected_sentences = [
        "Given I have the following courses in my university:",
        "When I consolidate the database into 'courses.txt'",
        "Then I see the 1st line of 'courses.txt' has 'Computer Science:5'",
        "And I see the 2nd line of 'courses.txt' has 'Nutrition:4'",
    ]

    for step, expected_sentence in zip(scenario.steps, expected_sentences):
        assert_equals(type(step), Step)
        assert_equals(step.sentence, expected_sentence)

    assert_equals(scenario.steps[0].keys, ('Name', 'Duration'))
    assert_equals(
        scenario.steps[0].data_list,
        [
            {'Name': 'Computer Science', 'Duration': '5 years'},
            {'Name': 'Nutrition', 'Duration': '4 years'},
        ]
    )
