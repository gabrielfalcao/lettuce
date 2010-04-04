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
from lettuce import registry
from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.terrain import world
from lettuce.core import Feature


FEATURE1 = '''
Feature: Before and After callbacks all along lettuce
    Scenario: Before and After steps
        Given I append "during" to states
'''

FEATURE2 = '''
Feature: Before and After callbacks all along lettuce
    Scenario: Before and After scenarios
        Given I append "during" to states

    Scenario: Again
        Given I append "during" to states
'''

def test_world():
    "lettuce.terrain.world can be monkey patched at will"

    def set_world():
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

def test_after_each_step_is_executed_before_each_step():
    "terrain.before.each_step and terrain.after.each_step decorators"
    world.step_states = []
    @before.each_step
    def set_state_to_before(step):
        world.step_states.append('before')
        expected = 'Given I append "during" to states'
        if step.sentence != expected:
            raise TypeError('%r != %r' % (step.sentence, expected))

    @step('append "during" to states')
    def append_during_to_step_states():
        world.step_states.append("during")

    @after.each_step
    def set_state_to_after(step):
        world.step_states.append('after')
        expected = 'Given I append "during" to states'
        if step.sentence != expected:
            raise TypeError('%r != %r' % (step.sentence, expected))

    feature = Feature.from_string(FEATURE1)
    feature.run()

    assert_equals(world.step_states, ['before', 'during', 'after'])

def test_after_each_scenario_is_executed_before_each_scenario():
    "terrain.before.each_scenario and terrain.after.each_scenario decorators"
    world.scenario_steps = []

    @before.each_scenario
    def set_state_to_before(scenario):
        world.scenario_steps.append('before')

    @step('append "during" to states')
    def append_during_to_scenario_steps():
        world.scenario_steps.append("during")

    @after.each_scenario
    def set_state_to_after(scenario):
        world.scenario_steps.append('after')

    feature = Feature.from_string(FEATURE2)
    feature.run()

    assert_equals(
        world.scenario_steps,
        ['before', 'during', 'after', 'before', 'during', 'after']
    )

def test_after_each_feature_is_executed_before_each_feature():
    "terrain.before.each_feature and terrain.after.each_feature decorators"
    world.feature_steps = []

    @before.each_feature
    def set_state_to_before(feature):
        world.feature_steps.append('before')

    @step('append "during" to states')
    def append_during_to_feature_steps():
        world.feature_steps.append("during")

    @after.each_feature
    def set_state_to_after(feature):
        world.feature_steps.append('after')

    feature = Feature.from_string(FEATURE2)
    feature.run()

    assert_equals(
        world.feature_steps,
        ['before', 'during', 'during', 'after']
    )

