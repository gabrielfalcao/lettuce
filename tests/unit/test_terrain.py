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
from nose.tools import assert_equals

from lettuce import step
from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.core import Feature

FEATURE = '''
Feature: Before and After callbacks all along lettuce
    Scenario: Before and After steps
        Given I append "during" to states

    Scenario: Before and After scenarios
        Given I append "during" to states

'''

def test_world():
    "lettuce.terrain.world can be monkey patched at will"

    def set_world():
        from lettuce.terrain import world
        world.was_set = True

    def test_does_not_have():
        from lettuce.terrain import world
        assert not hasattr(world, 'was_set')

    def test_does_have():
        from lettuce.terrain import world
        assert hasattr(world, 'was_set')

    test_does_not_have()
    set_world()
    test_does_have()

def _test_after_each_step_is_executed_before_each_step():
    "terrain.before.each_step and terrain.after.each_step decorators"
    step_states = []

    @before.each_step
    def set_state_to_before(step):
        assert_equals(step.sentence, 'Given I append "during" to step_states')
        step_states.append('before')


    @step('append "during" to step_states')
    def append_during_to_step_states():
        step_states.append("during")

    @after.each_step
    def set_state_to_after(step):
        assert_equals(step.sentence, 'Given I append "during" to step_states')
        step_states.append('after')


    feature = Feature.from_string(FEATURE)
    feature.run()

    assert_equals(step_states, ['before', 'during', 'after'])

def _test_after_each_scenario_is_executed_before_each_scenario():
    "terrain.before.each_scenario and terrain.after.each_scenario decorators"
    scenario_steps = []

    @before.each_scenario
    def set_state_to_before(scenario):
        if scenario.name == 'Before and After steps':
            scenario_steps.append('before')
        else:
            scenario_steps.append('almost during')


    @step('append "during" to scenario_steps')
    def append_during_to_scenario_steps():
        scenario_steps.append("during")

    @after.each_scenario
    def set_state_to_after(scenario):
        if scenario.name == 'Before and After scenarios':
            scenario_steps.append('almost after')
        else:
            scenario_steps.append('after')

    feature = Feature.from_string(FEATURE)
    feature.run()

    assert_equals(
        scenario_steps,
        ['before', 'almost during', 'during', 'almost after', 'after']
    )

