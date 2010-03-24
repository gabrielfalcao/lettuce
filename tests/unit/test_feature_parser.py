# -*- coding: utf-8 -*-
# <Lettuce - Behavior-driven design for python>
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

FEATURE1 = """
Feature: Rent movies
    Scenario: Renting a featured movie
        Given I have the following movies in my database
           | Name                    | Rating  | New | Available |
           | Matrix Revolutions      | 4 stars | no  | 6         |
           | Iron Man 2              | 5 stars | yes | 11        |
        When the client 'John Doe' rents 'Iron man 2'
        Then he needs to pay 10 bucks

    Scenario: Renting a non-featured movie
        Given I have the following movies in my database
           | Name                    | Rating  | New | Available |
           | A night at the museum 2 | 3 stars | yes | 9         |
           | Matrix Revolutions      | 4 stars | no  | 6         |
        When the client 'Mary Doe' rents 'Matrix Revolutions'
        Then she needs to pay 6 bucks

    Scenario: Renting two movies allows client to take one more without charge
        Given I have the following movies in my database
           | Name                    | Rating  | New | Available |
           | A night at the museum 2 | 3 stars | yes | 9         |
           | Matrix Revolutions      | 4 stars | no  | 6         |
           | Iron Man 2              | 5 stars | yes | 11        |
        When the client 'Jack' rents 'Iron man 2'
        And also rents 'Iron man 2' and 'A night at the museum 2'
        Then he needs to pay 16 bucks
"""

from lettuce.core import Step
from lettuce.core import Scenario
from lettuce.core import Feature
from nose.tools import assert_equals

def test_scenario_has_name():
    "It should extract the description string from the scenario"

    feature = Feature.from_string(FEATURE1)

    assert isinstance(feature, Feature)

    assert_equals(
        feature.description,
        "Rent movies"
    )

def test_feature_has_scenarios():
    "A feature object should have a list of scenarios"

    feature = Feature.from_string(FEATURE1)

    assert_equals(type(feature.scenarios), list)
    assert_equals(len(feature.scenarios), 3, "It should have 3 scenarios")

    expected_scenario_names = [
        "Renting a featured movie",
        "Renting a non-featured movie",
        "Renting two movies allows client to take one more without charge",
    ]

    for scenario, expected_name in zip(feature.scenarios, expected_scenario_names):
        assert_equals(type(scenario), Scenario)
        assert_equals(scenario.name, expected_name)

    assert_equals(feature.scenarios[1].steps[0].keys, ('Name', 'Rating', 'New', 'Available'))
    assert_equals(
        feature.scenarios[1].steps[0].data_list,
        [
            {'Name': 'A night at the museum 2', 'Rating': '3 stars', 'New': 'yes', 'Available': '9'},
            {'Name': 'Matrix Revolutions', 'Rating': '4 stars', 'New': 'no', 'Available': '6'},
        ]
    )
