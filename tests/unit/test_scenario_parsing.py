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

OUTLINED_SCENARIO = """
Scenario Outline: Add two numbers
    Given I have entered <input_1> into the calculator
    And I have entered <input_2> into the calculator
    When I press <button>
    Then the result should be <output> on the screen

    Examples:
      | input_1 | input_2 | button | output |
      | 20      | 30      | add    | 50     |
      | 2       | 5       | add    | 7      |
      | 0       | 40      | add    | 40     |
"""

OUTLINED_SCENARIO_WITH_SUBSTITUTIONS_IN_TABLE = """
Scenario Outline: Bad configuration should fail
    Given I provide the following configuration:
       | Parameter | Value |
       |     a     |  <a>  |
       |     b     |  <b>  |
    When I run the program
    Then it should fail hard-core

Examples:
    | a | b |
    | 1 | 2 |
    | 2 | 4 |
"""

OUTLINED_FEATURE = """
    Feature: Do many things at once
        In order to automate tests
        As a automation freaky
        I want to use scenario outlines

        Scenario Outline: Add two numbers wisely
            Given I have entered <input_1> into the calculator
            And I have entered <input_2> into the calculator
            When I press <button>
            Then the result should be <output> on the screen

        Examples:
            | input_1 | input_2 | button | output |
            | 20      | 30      | add    | 50     |
            | 2       | 5       | add    | 7      |
            | 0       | 40      | add    | 40     |
"""

OUTLINED_FEATURE_WITH_MANY = """
    Feature: Full-featured feature
        Scenario Outline: Do something
            Given I have entered <input_1> into the <input_2>

        Examples:
            | input_1 | input_2 |
            | ok      | fail    |
            | fail    | ok      |

        Scenario: Do something else
          Given I am fine

        Scenario: Worked!
          Given it works
          When I look for something
          Then I find it

        Scenario Outline: Add two numbers wisely
            Given I have entered <input_1> into the calculator
            And I have entered <input_2> into the calculator
            When I press <button>
            Then the result should be <output> on the screen

        Examples:
            | input_1 | input_2 | button | output |
            | 20      | 30      | add    | 50     |
            | 2       | 5       | add    | 7      |
            | 0       | 40      | add    | 40     |

        Examples:
            | input_1 | input_2 | button | output |
            | 5       | 7       | add    | 12     |

"""

SCENARIO_FAILED = """
Scenario: Adding some students to my university database
       | Name               | Duration |
       | Computer Science   | 5 years  |
       | Nutrition          | 4 years  |
    When I consolidate the database into 'courses.txt'
    Then I see the 1st line of 'courses.txt' has 'Computer Science:5'
    And I see the 2nd line of 'courses.txt' has 'Nutrition:4'
"""

OUTLINED_SCENARIO_WITH_COMMENTS_ON_EXAMPLES = """
Scenario Outline: Add two numbers
    Given I have entered <input_1> into the calculator
    And I have entered <input_2> into the calculator
    When I press <button>
    Then the result should be <output> on the screen

    Examples:
      | input_1 | input_2 | button | output |
      | 20      | 30      | add    | 50     |
      #| 2       | 5       | add    | 7      |
      | 0       | 40      | add    | 40     |
    # end of the scenario
"""

OUTLINED_SCENARIO_WITH_MORE_THAN_ONE_EXAMPLES_BLOCK = """
Scenario Outline: Add two numbers
    Given I have entered <input_1> into the calculator
    And I have entered <input_2> into the calculator
    When I press <button>
    Then the result should be <output> on the screen

    Examples:
      | input_1 | input_2 | button | output |
      | 20      | 30      | add    | 50     |
      | 2       | 5       | add    | 7      |
      | 0       | 40      | add    | 40     |

    Examples:
      | input_1 | input_2 | button | output |
      | 20      | 33      | add    | 53     |
      | 12      | 40      | add    | 52     |
"""

COMMENTED_SCENARIO = """
Scenario: Adding some students to my university database
    Given I have the following courses in my university:
       | Name               | Duration |
       | Computer Science   | 5 years  |
       | Nutrition          | 4 years  |
    When I consolidate the database into 'courses.txt'
    Then I see the 1st line of 'courses.txt' has 'Computer Science:5'
    And I see the 2nd line of 'courses.txt' has 'Nutrition:4'

# Scenario: Adding some students to my university database
#     Given I have the following courses in my university:
#        | Name               | Duration |
#        | Computer Science   | 5 years  |
#        | Nutrition          | 4 years  |
#     When I consolidate the database into 'courses.txt'
#     Then I see the 1st line of 'courses.txt' has 'Computer Science:5'
#     And I see the 2nd line of 'courses.txt' has 'Nutrition:4'

"""

TAGGED_FEATURE_WITH_MANY = """
    @outer-tag @outer2
    Feature: Full-featured feature
             feature description line 1
             line 2
        @something-tag
        Scenario Outline: Do something
            Given I have entered <input_1> into the <input_2>

        Examples:
            | input_1 | input_2 |
            | ok      | fail    |
            | fail    | ok      |

        @something-else-tag
        Scenario: Do something else
          Given I am fine

        Scenario: Worked!
          Given it works
          When I look for something
          Then I find a multi-line string:
          \"\"\"
          what if I put a tag
          @on-one
          of these lines? 
          \"\"\"

        Scenario Outline: Add two numbers wisely
            Given I have entered <input_1> into the calculator
            And I have entered <input_2> into the calculator
            When I press <button>
            Then the result should be <output> on the screen

        Examples:
            | input_1 | input_2 | button | output |
            | 20      | 30      | add    | 50     |
            | 2       | 5       | add    | 7      |
            | 0       | 40      | add    | 40     |

        Examples:
            | input_1 | input_2 | button | output |
            | 5       | 7       | add    | 12     |

"""


from lettuce.core import Step
from lettuce.core import Scenario
from lettuce.core import Feature
from lettuce.exceptions import LettuceSyntaxError

from nose.tools import assert_equals
from nose.tools import assert_raises

def test_scenario_has_name():
    "It should extract the name of the scenario"

    scenario = Scenario.from_string(SCENARIO1)

    assert isinstance(scenario, Scenario)

    assert_equals(
        scenario.name,
        "Adding some students to my university database"
    )

def test_scenario_has_repr():
    "Scenario implements __repr__ nicely"
    scenario = Scenario.from_string(SCENARIO1)
    assert_equals(
        repr(scenario),
        '<Scenario: "Adding some students to my university database">'
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
        scenario.steps[0].hashes,
        [
            {'Name': 'Computer Science', 'Duration': '5 years'},
            {'Name': 'Nutrition', 'Duration': '4 years'},
        ]
    )

def test_scenario_may_own_outlines():
    "A scenario may own outlines"
    scenario = Scenario.from_string(OUTLINED_SCENARIO)

    assert_equals(len(scenario.steps), 4)
    expected_sentences = [
        'Given I have entered <input_1> into the calculator',
        'And I have entered <input_2> into the calculator',
        'When I press <button>',
        'Then the result should be <output> on the screen',
    ]

    for step, expected_sentence in zip(scenario.steps, expected_sentences):
        assert_equals(type(step), Step)
        assert_equals(step.sentence, expected_sentence)

    assert_equals(scenario.name, "Add two numbers")
    assert_equals(
        scenario.outlines,
        [
            {'input_1': '20', 'input_2': '30', 'button': 'add', 'output': '50'},
            {'input_1': '2', 'input_2': '5', 'button': 'add', 'output': '7'},
            {'input_1': '0', 'input_2': '40', 'button': 'add', 'output': '40'},
        ]
    )

def test_steps_parsed_by_scenarios_has_scenarios():
    "Steps parsed by scenarios has scenarios"
    scenario = Scenario.from_string(SCENARIO1)
    for step in scenario.steps:
        assert_equals(step.scenario, scenario)

def test_scenario_sentences_can_be_solved():
    "A scenario with outlines may solve its sentences"
    scenario = Scenario.from_string(OUTLINED_SCENARIO)

    assert_equals(len(scenario.solved_steps), 12)
    expected_sentences = [
        'Given I have entered 20 into the calculator',
        'And I have entered 30 into the calculator',
        'When I press add',
        'Then the result should be 50 on the screen',
        'Given I have entered 2 into the calculator',
        'And I have entered 5 into the calculator',
        'When I press add',
        'Then the result should be 7 on the screen',
        'Given I have entered 0 into the calculator',
        'And I have entered 40 into the calculator',
        'When I press add',
        'Then the result should be 40 on the screen',
    ]

    for step, expected_sentence in zip(scenario.solved_steps, expected_sentences):
        assert_equals(type(step), Step)
        assert_equals(step.sentence, expected_sentence)

def test_scenario_tables_are_solved_against_outlines():
    "Outline substitution should apply to tables within a scenario"
    expected_hashes_per_step = [
            # a = 1, b = 2
            [{'Parameter': 'a', 'Value': '1'}, {'Parameter': 'b', 'Value': '2'}], # Given ...
            [], # When I run the program
            [], # Then I crash hard-core

            # a = 2, b = 4
            [{'Parameter': 'a', 'Value': '2'}, {'Parameter': 'b', 'Value': '4'}],
            [],
            []
        ]
    
    scenario = Scenario.from_string(OUTLINED_SCENARIO_WITH_SUBSTITUTIONS_IN_TABLE)
    for step, expected_hashes in zip(scenario.solved_steps, expected_hashes_per_step):
        assert_equals(type(step), Step)
        assert_equals(step.hashes, expected_hashes)

def test_solved_steps_also_have_scenario_as_attribute():
    "Steps solved in scenario outlines also have scenario as attribute"
    scenario = Scenario.from_string(OUTLINED_SCENARIO)
    for step in scenario.solved_steps:
        assert_equals(step.scenario, scenario)

def test_scenario_outlines_within_feature():
    "Solving scenario outlines within a feature"
    feature = Feature.from_string(OUTLINED_FEATURE)
    scenario = feature.scenarios[0]

    assert_equals(len(scenario.solved_steps), 12)
    expected_sentences = [
        'Given I have entered 20 into the calculator',
        'And I have entered 30 into the calculator',
        'When I press add',
        'Then the result should be 50 on the screen',
        'Given I have entered 2 into the calculator',
        'And I have entered 5 into the calculator',
        'When I press add',
        'Then the result should be 7 on the screen',
        'Given I have entered 0 into the calculator',
        'And I have entered 40 into the calculator',
        'When I press add',
        'Then the result should be 40 on the screen',
    ]

    for step, expected_sentence in zip(scenario.solved_steps, expected_sentences):
        assert_equals(type(step), Step)
        assert_equals(step.sentence, expected_sentence)

def test_full_featured_feature():
    "Solving scenarios within a full-featured feature"
    feature = Feature.from_string(OUTLINED_FEATURE_WITH_MANY)
    scenario1, scenario2, scenario3, scenario4 = feature.scenarios

    assert_equals(scenario1.name, 'Do something')
    assert_equals(scenario2.name, 'Do something else')
    assert_equals(scenario3.name, 'Worked!')
    assert_equals(scenario4.name, 'Add two numbers wisely')

    assert_equals(len(scenario1.solved_steps), 2)
    expected_sentences = [
        'Given I have entered ok into the fail',
        'Given I have entered fail into the ok',
    ]
    for step, expected_sentence in zip(scenario1.solved_steps, expected_sentences):
        assert_equals(step.sentence, expected_sentence)

    expected_evaluated = (
        (
            {'button': 'add', 'input_1': '20', 'input_2': '30', 'output': '50'}, [
                'Given I have entered 20 into the calculator',
                'And I have entered 30 into the calculator',
                'When I press add',
                'Then the result should be 50 on the screen',
            ]
        ),
        (
            {'button': 'add', 'input_1': '2', 'input_2': '5', 'output': '7'}, [
                'Given I have entered 2 into the calculator',
                'And I have entered 5 into the calculator',
                'When I press add',
                'Then the result should be 7 on the screen',
                ]
        ),
        (
            {'button': 'add', 'input_1': '0', 'input_2': '40', 'output': '40'}, [
                'Given I have entered 0 into the calculator',
                'And I have entered 40 into the calculator',
                'When I press add',
                'Then the result should be 40 on the screen',
            ],
        ),
        (
            {'button': 'add', 'input_1': '5', 'input_2': '7', 'output': '12'}, [
                'Given I have entered 5 into the calculator',
                'And I have entered 7 into the calculator',
                'When I press add',
                'Then the result should be 12 on the screen',
            ],
        )
    )
    for ((got_examples, got_steps), (expected_examples, expected_steps)) in zip(scenario4.evaluated, expected_evaluated):
        sentences_of = lambda x: x.sentence
        assert_equals(got_examples, expected_examples)
        assert_equals(map(sentences_of, got_steps), expected_steps)

def test_scenario_with_table_and_no_step_fails():
    "A step table imediately after the scenario line, without step line fails"

    assert_raises(LettuceSyntaxError, Scenario.from_string, SCENARIO_FAILED)

def test_scenario_ignore_commented_lines_from_examples():
    "Comments on scenario example should be ignored"
    scenario = Scenario.from_string(OUTLINED_SCENARIO_WITH_COMMENTS_ON_EXAMPLES)

    assert_equals(
        scenario.outlines,
        [
            {'input_1': '20', 'input_2': '30', 'button': 'add', 'output': '50'},
            {'input_1': '0', 'input_2': '40', 'button': 'add', 'output': '40'},
        ]
    )

def test_scenario_aggregate_all_examples_blocks():
    "All scenario's examples block should be translated to outlines"
    scenario = Scenario.from_string(OUTLINED_SCENARIO_WITH_MORE_THAN_ONE_EXAMPLES_BLOCK)

    assert_equals(
        scenario.outlines,
        [
            {'input_1': '20', 'input_2': '30', 'button': 'add', 'output': '50'},
            {'input_1': '2', 'input_2': '5', 'button': 'add', 'output': '7'},
            {'input_1': '0', 'input_2': '40', 'button': 'add', 'output': '40'},
            {'input_1': '20', 'input_2': '33', 'button': 'add', 'output': '53'},
            {'input_1': '12', 'input_2': '40', 'button': 'add', 'output': '52'},
        ]
    )

def test_commented_scenarios():
    "A scenario string that contains lines starting with '#' will be commented"
    scenario = Scenario.from_string(COMMENTED_SCENARIO)
    assert_equals(scenario.name, u'Adding some students to my university database')
    assert_equals(len(scenario.steps), 4)

def test_fully_tagged_feature():
    "Check that tags are parsed correctly"
    feature = Feature.from_string(TAGGED_FEATURE_WITH_MANY)
    assert_equals(feature.description, u'feature description line 1\nline 2')
    assert_equals(len(feature.scenarios), 4)
    scenario1, scenario2, scenario3, scenario4 = feature.scenarios

    assert_equals(scenario1.name, 'Do something')
    assert_equals(scenario2.name, 'Do something else')
    assert_equals(scenario3.name, 'Worked!')
    assert_equals(scenario4.name, 'Add two numbers wisely')
    # Check tags 
    assert_equals(scenario1.tags, ["outer-tag", "outer2", "something-tag"])
    assert_equals(scenario2.tags, ["outer-tag", "outer2", "something-else-tag"])
    assert_equals(scenario3.tags, ["outer-tag", "outer2"])
    assert_equals(scenario4.tags, ["outer-tag", "outer2"])