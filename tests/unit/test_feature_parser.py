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

from lettuce.core import Scenario
from lettuce.core import Feature
from nose.tools import assert_equals

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

FEATURE2 = """
Feature: Division
      In order to avoid silly mistakes
      Cashiers must be able to calculate a fraction

      Scenario: Regular numbers
            * I have entered 3 into the calculator
            * I have entered 2 into the calculator
            * I press divide
            * the result should be 1.5 on the screen
"""

FEATURE3 = """
Feature: A long line as feature name will define the max length of the feature
  In order to describe my features
  I want to add description on them
  Scenario: Regular numbers
    Nothing to do
"""

FEATURE4 = """
Feature: Big sentence
  As a clever guy
  I want to describe this Feature
  So that I can take care of my Scenario
  Scenario: Regular numbers
    Given a huge sentence, that have so many characters
    And another one, very tiny
"""

FEATURE5 = """
Feature: Big table
  Scenario: Regular numbers
    Given that I have these items:
      | description                                                               |
      | this is such a huge description within a table, the maxlengh will be huge |
      | this is another description within a table                                |
"""

FEATURE6 = """
Feature: Big scenario outline
  Scenario: Regular numbers
    Given I do fill 'description' with '<value_two>'
  Examples:
    | value_two                                                               |
    | this is such a huge value within a table, the maxlengh will be damn big |
    | this is another description within a table                              |

"""

FEATURE7 = """
Feature: Big table
  Scenario: Regular numbers
    Given that I have these items:
      | description-long-as-hell | name-that-will-make-my-max-length-big |
      | one                      | john                                  |
      | two                      | baby                                  |
"""

FEATURE8 = """
Feature: Big scenario outline
  Scenario: big scenario outlines
    Given I do fill 'description' with '<value_two>'

  Examples:
    | value_two_thousand_and_three | another_one | and_even_bigger |
    | 1                            | um          | one             |
    | 2                            | dois        | two             |
"""

FEATURE9 = """
Feature: Big scenario outline
  Scenario: big scenario outlines
    Given I do fill 'description' with '<value_two>'

  Examples:
    | value_two_thousand_and_three_biiiiiiiiiiiiiiiiiiiiiiiiiiiiig |
    | 1                                                            |
    | 2                                                            |
    | 3                                                            |
"""


def test_feature_has_repr():
    "Feature implements __repr__ nicely"
    feature = Feature.from_string(FEATURE1)
    assert_equals(repr(feature), '<Feature: "Rent movies">')

def test_scenario_has_name():
    "It should extract the name string from the scenario"

    feature = Feature.from_string(FEATURE1)

    assert isinstance(feature, Feature)

    assert_equals(
        feature.name,
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
        feature.scenarios[1].steps[0].hashes,
        [
            {'Name': 'A night at the museum 2', 'Rating': '3 stars', 'New': 'yes', 'Available': '9'},
            {'Name': 'Matrix Revolutions', 'Rating': '4 stars', 'New': 'no', 'Available': '6'},
        ]
    )

def test_can_parse_feature_description():
    "A feature object should have a description"

    feature = Feature.from_string(FEATURE2)

    assert_equals(
        feature.description,
        "In order to avoid silly mistakes\n"
        "Cashiers must be able to calculate a fraction"
    )
    expected_scenario_names = ["Regular numbers"]
    got_scenario_names = [s.name for s in feature.scenarios]

    assert_equals(expected_scenario_names, got_scenario_names)
    assert_equals(len(feature.scenarios[0].steps), 4)

    step1, step2, step3, step4 = feature.scenarios[0].steps

    assert_equals(step1.sentence, '* I have entered 3 into the calculator')
    assert_equals(step2.sentence, '* I have entered 2 into the calculator')
    assert_equals(step3.sentence, '* I press divide')
    assert_equals(step4.sentence, '* the result should be 1.5 on the screen')

def test_scenarios_parsed_by_feature_has_feature():
    "Scenarios parsed by features has feature"

    feature = Feature.from_string(FEATURE2)

    for scenario in feature.scenarios:
        assert_equals(scenario.feature, feature)

def test_feature_max_length_on_scenario():
    "The max length of a feature considering when the scenario is longer than " \
    "the remaining things"

    feature = Feature.from_string(FEATURE1)
    assert_equals(feature.max_length, 76)

def test_feature_max_length_on_feature_description():
    "The max length of a feature considering when one of the description lines " \
    "of the feature is longer than the remaining things"

    feature = Feature.from_string(FEATURE2)
    assert_equals(feature.max_length, 47)

def test_feature_max_length_on_feature_name():
    "The max length of a feature considering when the name of the feature " \
    "is longer than the remaining things"

    feature = Feature.from_string(FEATURE3)
    assert_equals(feature.max_length, 78)

def test_feature_max_length_on_step_sentence():
    "The max length of a feature considering when the some of the step sentences " \
    "is longer than the remaining things"

    feature = Feature.from_string(FEATURE4)
    assert_equals(feature.max_length, 55)

def test_feature_max_length_on_step_with_table():
    "The max length of a feature considering when the table of some of the steps " \
    "is longer than the remaining things"

    feature = Feature.from_string(FEATURE5)
    assert_equals(feature.max_length, 83)

def test_feature_max_length_on_step_with_table_keys():
    "The max length of a feature considering when the table keys of some of the " \
    "steps are longer than the remaining things"

    feature = Feature.from_string(FEATURE7)
    assert_equals(feature.max_length, 74)

def test_feature_max_length_on_scenario_outline():
    "The max length of a feature considering when the table of some of the  " \
    "scenario oulines is longer than the remaining things"

    feature = Feature.from_string(FEATURE6)
    assert_equals(feature.max_length, 79)

def test_feature_max_length_on_scenario_outline_keys():
    "The max length of a feature considering when the table keys of the  " \
    "scenario oulines are longer than the remaining things"

    feature1 = Feature.from_string(FEATURE8)
    feature2 = Feature.from_string(FEATURE9)
    assert_equals(feature1.max_length, 68)
    assert_equals(feature2.max_length, 68)

def test_description_on_long_named_feature():
    "Can parse the description on long named features"
    feature = Feature.from_string(FEATURE3)
    assert_equals(
        feature.description,
        "In order to describe my features\n"
        "I want to add description on them"
    )

def test_description_on_big_sentenced_steps():
    "Can parse the description on long sentenced steps"
    feature = Feature.from_string(FEATURE4)
    assert_equals(
        feature.description,
        "As a clever guy\n"
        "I want to describe this Feature\n"
        "So that I can take care of my Scenario"
    )

