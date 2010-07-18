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
from lettuce import step
from lettuce import after
from lettuce import core
from lettuce import registry
from lettuce.core import Step
from lettuce.core import Feature
from nose.tools import assert_equals, with_setup

FEATURE1 = """
Feature: Count steps ran
    Scenario: Total of steps ran
        Given I have a defined step
        When other step fails
        Then it won't reach here
        Then I have a defined step
"""

FEATURE2 = """
Feature: Find undefined steps
    Scenario: Undefined step can be pointed
        Given I have a defined step
        Then this one has no definition
        And this one also
"""

FEATURE3 = """
Feature: Lettuce can ignore case
    Scenario: On step definitions
        Given I define a step
        And DEFINE a STEP
        And also define A sTeP
"""

FEATURE4 = '''
Feature: My steps are rocking!
    Scenario: Step definition receive regex matched groups as parameters
        Given a person called "John Doe"
'''

FEATURE5 = '''
Feature: My steps are rocking!
    Scenario: Step definition receive regex matched named groups as parameters
        When a foreign at "Rio de Janeiro"
'''

FEATURE6 = '''
Feature: My steps are rocking!
    Scenario: Step definition receive regex matched named groups as parameters
        Then he gets a caipirinha
'''

FEATURE7 = """
Feature: Many scenarios
  Scenario: 1st one
    Given I have a defined step

  Scenario: 2nd one
    Given I have a defined step

  Scenario: 3rd one
    Given I have a defined step

  Scenario: 4th one
    Given I have a defined step

  Scenario: 5th one
    Given I have a defined step

"""

FEATURE8 = """
Feature: Count step definitions with exceptions as failing steps
  Scenario: Raising exception
    Given I have a defined step
    When I have a step that raises an exception
    Then this step will be skipped
"""

def step_runner_environ():
    "Make sure the test environment is what is expected"

    from lettuce import registry
    registry.clear()

    @step('I have a defined step')
    def have_a_defined_step(*args, **kw):
        assert True

    @step('other step fails')
    def and_another(*args, **kw):
        assert False, 'It should fail'

    @step("define a step")
    def define_a_step(*args, **kw):
        assert True

    @step(u'When I have a step that raises an exception')
    def raises_exception(step):
        raise Exception()

@with_setup(step_runner_environ)
def test_can_count_steps_and_its_states():
    "The scenario result has the steps passed, failed and skipped steps. " \
    "And total steps as well."

    f = Feature.from_string(FEATURE1)
    feature_result = f.run()

    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 1)
    assert_equals(len(scenario_result.steps_failed), 1)
    assert_equals(len(scenario_result.steps_undefined), 1)
    assert_equals(len(scenario_result.steps_skipped), 1)
    assert_equals(scenario_result.total_steps, 4)

@with_setup(step_runner_environ)
def test_can_point_undefined_steps():
    "The scenario result has also the undefined steps."

    f = Feature.from_string(FEATURE2)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_undefined), 2)
    assert_equals(len(scenario_result.steps_passed), 1)
    assert_equals(scenario_result.total_steps, 3)

    undefined1 = scenario_result.steps_undefined[0]
    undefined2 = scenario_result.steps_undefined[1]

    assert_equals(undefined1.sentence, 'Then this one has no definition')
    assert_equals(undefined2.sentence, 'And this one also')

@with_setup(step_runner_environ)
def test_can_figure_out_why_has_failed():
    "It can figure out why the test has failed"

    f = Feature.from_string(FEATURE1)
    feature_result = f.run()

    scenario_result = feature_result.scenario_results[0]
    failed_step = scenario_result.steps_failed[0]

    assert_equals(failed_step.why.cause, 'It should fail')
    assert 'Traceback (most recent call last):' in failed_step.why.traceback
    assert 'AssertionError: It should fail' in failed_step.why.traceback
    assert_equals(type(failed_step.why.exception), AssertionError)

@with_setup(step_runner_environ)
def test_skipped_steps_can_be_retrieved_as_steps():
    "Skipped steps can be retrieved as steps"

    f = Feature.from_string(FEATURE1)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]
    for step in scenario_result.steps_skipped:
        assert_equals(type(step), Step)

@with_setup(step_runner_environ)
def test_ignore_case_on_step_definitions():
    "By default lettuce ignore case on step definitions"

    f = Feature.from_string(FEATURE3)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 3)
    assert_equals(scenario_result.total_steps, 3)
    assert all([s.has_definition for s in scenario_result.scenario.steps])

@with_setup(step_runner_environ)
def test_doesnt_ignore_case():
    "Lettuce can, optionally consider case on step definitions"

    f = Feature.from_string(FEATURE3)
    feature_result = f.run(ignore_case=False)
    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 1)
    assert_equals(len(scenario_result.steps_undefined), 2)
    assert_equals(scenario_result.total_steps, 3)
    assert not all([s.has_definition for s in scenario_result.scenario.steps])

@with_setup(step_runner_environ)
def test_steps_are_aware_of_its_definitions():
    "Steps are aware of its definitions line numbers and file names"

    f = Feature.from_string(FEATURE1)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]

    for step in scenario_result.steps_passed:
        assert step.has_definition

    step1 = scenario_result.steps_passed[0]

    assert_equals(step1.defined_at.line, 102)
    assert_equals(step1.defined_at.file, core.fs.relpath(__file__.rstrip("c")))

@with_setup(step_runner_environ)
def test_steps_that_match_groups_takes_them_as_parameters():
    "Steps that match groups takes them as parameters"
    @step(r'Given a ([^\s]+) called "(.*)"')
    def given_what_named(step, what, name):
        assert_equals(what, 'person')
        assert_equals(name, 'John Doe')

    f = Feature.from_string(FEATURE4)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 1)
    assert_equals(scenario_result.total_steps, 1)

@with_setup(step_runner_environ)
def test_steps_that_match_named_groups_takes_them_as_parameters():
    "Steps that match named groups takes them as parameters"
    @step(r'When a (?P<what>\w+) at "(?P<city>.*)"')
    def given_action_named(step, what, city):
        assert_equals(what, 'foreign')
        assert_equals(city, 'Rio de Janeiro')

    f = Feature.from_string(FEATURE5)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 1)
    assert_equals(scenario_result.total_steps, 1)

@with_setup(step_runner_environ)
def test_steps_that_match_groups_and_named_groups_takes_just_named_as_params():
    "Steps that match groups and named groups takes just the named as parameters"
    @step(r'(he|she) gets a (?P<what>\w+)')
    def given_action_named(step, what):
        assert_equals(what, 'caipirinha')

    f = Feature.from_string(FEATURE6)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 1)
    assert_equals(scenario_result.total_steps, 1)

@with_setup(step_runner_environ)
def test_step_definitions_takes_the_step_object_as_first_argument():
    "Step definitions takes step object as first argument"

    FEATURE = '''
    Feature: Steps as args
        Scenario: Steps as args
            When I define this one
    '''

    @step(r'When I define this one')
    def when_i_define_this_one(step):
        assert_equals(step.sentence, 'When I define this one')

    f = Feature.from_string(FEATURE)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 1)
    assert_equals(scenario_result.total_steps, 1)

@with_setup(step_runner_environ)
def test_feature_can_run_only_specified_scenarios():
    "Features can run only specified scenarios, by index + 1"

    feature = Feature.from_string(FEATURE7)

    scenarios_ran = []
    @after.each_scenario
    def just_register(scenario):
        scenarios_ran.append(scenario.name)

    feature.run(scenarios=(2, 5))
    assert_equals(scenarios_ran, ['2nd one', '5th one'])


@with_setup(step_runner_environ)
def test_count_raised_exceptions_as_failing_steps():
    "When a step definition raises an exception, it is marked as a failed step. "

    try:
        f = Feature.from_string(FEATURE8)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        assert_equals(len(scenario_result.steps_failed), 1)
    finally:
        registry.clear()

