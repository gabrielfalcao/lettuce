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

from lettuce import core
from nose.tools import assert_equals
from nose.tools import assert_not_equals

STEP_WITH_TABLE = u'''
Given I have the following items in my shelf:
      | name  | description                                           |
      | Glass | a nice glass to drink grape juice                     |
      | Pasta | a pasta to cook and eat with grape juice in the glass |
'''


def test_step_definition():
    "Step definition takes a function and a step, keeps its definition " \
    "relative path, and line + 1 (to consider the decorator)"

    def dumb():
        pass

    definition = core.StepDefinition("FOO BAR", dumb)
    assert_equals(definition.function, dumb)
    assert_equals(definition.file, core.fs.relpath(__file__).rstrip("c"))
    assert_equals(definition.line, 35)


def test_step_description():
    "Step description takes a line and filename, " \
          "and keeps the relative path for filename"

    description = core.StepDescription(10, __file__)
    assert_equals(description.file, core.fs.relpath(__file__))
    assert_not_equals(description.file, __file__)
    assert_equals(description.line, 10)


def test_scenario_description():
    "Scenario description takes a scenario, filename and " \
        "a string, and keeps the relative path for filename and line"

    string = '''
    asdasdasdasd
    8fg6f8g23o83g
    dfjdsfjsdScenario: NAMEOFSCENARIOjdkasbdkajsb
Fsdad
          Scenario: NAMEOFSCENARIO
 da  sodnasndjasdasd
    '''

    class ScenarioFake:
        name = 'NAMEOFSCENARIO'

    description = core.ScenarioDescription(
        ScenarioFake, __file__, string, core.Language())

    assert_equals(description.file, core.fs.relpath(__file__))
    assert_not_equals(description.file, __file__)
    assert_equals(description.line, 6)


def test_feature_description():
    "Feature description takes a feature, filename and original " \
        "string, and keeps the relative path for filename, line " \
        "and description lines"

    string = u'''
    # lang: en-us
    Feature: FEATURE NAME! #@@$%ˆ&*)(*%$E#
    here comes
    the description
    of the scenario
    really!
    '''

    class FakeFeature:
        description = 'the description\nof the scenario\n'

    description = core.FeatureDescription(
        FakeFeature, __file__, string, core.Language())

    assert_equals(description.file, core.fs.relpath(__file__))
    assert_not_equals(description.file, __file__)
    assert_equals(description.line, 3)
    assert_equals(description.description_at, (5, 6))


def test_step_represent_string_when_not_defined():
    "Step.represent_string behaviour when not defined"

    class FakeFeature:
        max_length = 10

    class FakeScenario:
        feature = FakeFeature

    relative_path = core.fs.relpath(__file__)
    step = core.Step('some sentence', '', 239, __file__)
    step.scenario = FakeScenario

    assert_equals(
        step.represent_string('test'),
        "    test   # %s:239\n" % relative_path,
    )


def test_step_represent_string_when_defined():
    "Step.represent_string behaviour when defined"

    class FakeFeature:
        max_length = 10

    class FakeScenario:
        feature = FakeFeature

    class FakeScenarioDefinition:
        line = 421
        file = 'should/be/filename'

    step = core.Step('some sentence', '', 239, "not a file")
    step.scenario = FakeScenario
    step.defined_at = FakeScenarioDefinition
    assert_equals(
        step.represent_string('foobar'),
        "    foobar # should/be/filename:421\n",
    )


def test_step_represent_table():
    "Step.represent_hashes"

    step = core.Step.from_string(STEP_WITH_TABLE)

    assert_equals(
        step.represent_hashes(),
        '      | name  | description                                           |\n'
        '      | Glass | a nice glass to drink grape juice                     |\n'
        '      | Pasta | a pasta to cook and eat with grape juice in the glass |\n'
    )

SCENARIO_OUTLINE = u'''
Scenario: Regular numbers
                               Given I do fill description with '<value_one>'
                               And then, age with with '<and_other>'
Examples:
         |     value_one       | and_other                   |
         | first| primeiro |
         |second |segundo|
'''


def test_scenario_outline_represent_examples():
    "Step.represent_hashes"

    step = core.Scenario.from_string(SCENARIO_OUTLINE)

    assert_equals(
        step.represent_examples(),
        '    | value_one | and_other |\n'
        '    | first     | primeiro  |\n'
        '    | second    | segundo   |\n'
    )


def test_tagchecker_maches_all_if_not_specified():
    "Check anything matches if no tags specified"
    checker = core.TagChecker()
    assert_equals(checker.tags_match([]), True)
    assert_equals(checker.tags_match(["one"]), True)
    assert_equals(checker.tags_match(["one", "two"]), True)


def test_tagchecker_matching_aingle_tag():
    u"Check single required tag"
    checker = core.TagChecker(["red"])
    assert_equals(checker.tags_match([]), False)
    assert_equals(checker.tags_match(["one"]), False)
    assert_equals(checker.tags_match(["one", "two"]), False)
    assert_equals(checker.tags_match(["one", "red"]), True)


def test_multiple_required_tags():
    u"Check multiple required tags (AND)"
    checker = core.TagChecker(["red,green"])
    assert_equals(checker.tags_match([]), False)
    assert_equals(checker.tags_match(["one"]), False)
    assert_equals(checker.tags_match(["one", "red"]), False)
    assert_equals(checker.tags_match(["one", "green"]), False)
    assert_equals(checker.tags_match(["one", "red", "green"]), True)
    assert_equals(checker.tags_match(["red", "green"]), True)


def test_multiple_tags():
    u"Check multiple tags (OR)"
    checker = core.TagChecker(["red", "green"])
    assert_equals(checker.tags_match([]), False)
    assert_equals(checker.tags_match(["one"]), False)
    assert_equals(checker.tags_match(["one", "red"]), True)
    assert_equals(checker.tags_match(["one", "green"]), True)
    assert_equals(checker.tags_match(["one", "red", "green"]), True)
    assert_equals(checker.tags_match(["red", "green"]), True)


def test_negative_tags():
    u"Check negative tags"
    checker = core.TagChecker(["~red"])
    assert_equals(checker.tags_match([]), True)
    assert_equals(checker.tags_match(["one"]), True)
    assert_equals(checker.tags_match(["one", "red"]), False)


def test_combining_negative_using_and():
    u"Check combination negative tags (NOT in AND)"
    checker = core.TagChecker(["~red,green"])
    assert_equals(checker.tags_match([]), False)
    assert_equals(checker.tags_match(["one"]), False)
    assert_equals(checker.tags_match(["one", "red"]), False)
    assert_equals(checker.tags_match(["one", "red", "green"]), False)
    assert_equals(checker.tags_match(["one", "green"]), True)


def test_remove_trailing_at_sign():
    u"Check at-signs are removed if supplied (e.g. command line)"
    checker = core.TagChecker(["@red"])
    assert_equals(checker.tags_to_run, ["red"])
    checker = core.TagChecker(["@red,~@blue"])
    assert_equals(checker.tags_to_run, ["red,~blue"])


def test_run_controller():
    rc = core.RunController()
    s = "fake scenario"
    assert_equals(rc.want_run_scenario(s), True)
    # Try with some positive delegates

    class PositiveDelegate():
        def want_run_scenario(self, scenario):
            return True

    class NegativeDelegate():
        def want_run_scenario(self, scenario):
            return False

    rc.add(PositiveDelegate())
    assert_equals(rc.want_run_scenario(s), True)
    # Two delegates
    rc.add(PositiveDelegate())
    assert_equals(rc.want_run_scenario(s), True)
    # Negative delegate on end
    rc.add(NegativeDelegate())
    assert_equals(rc.want_run_scenario(s), False)
    # Negative delegate on front
    rc = core.RunController()
    rc.add(NegativeDelegate())
    assert_equals(rc.want_run_scenario(s), False)
    # Negative delegate in middle
    rc = core.RunController()
    rc.add(PositiveDelegate())
    rc.add(NegativeDelegate())
    rc.add(PositiveDelegate())
    assert_equals(rc.want_run_scenario(s), False)
