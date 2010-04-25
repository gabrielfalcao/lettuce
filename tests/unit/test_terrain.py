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
from mox import Mox
from nose.tools import assert_equals

from lettuce import step
from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.terrain import world
from lettuce.core import Feature, TotalResult
from lettuce.registry import CALLBACK_REGISTRY

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
    def append_during_to_step_states(step):
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
    def append_during_to_scenario_steps(step):
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
    def append_during_to_feature_steps(step):
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

def test_after_each_all_is_executed_before_each_all():
    "terrain.before.each_all and terrain.after.each_all decorators"
    import lettuce
    from lettuce.fs import FeatureLoader
    world.all_steps = []

    mox = Mox()

    loader_mock = mox.CreateMock(FeatureLoader)
    mox.StubOutWithMock(lettuce.sys, 'path')
    mox.StubOutWithMock(lettuce, 'fs')
    mox.StubOutWithMock(lettuce.fs, 'FileSystem')
    mox.StubOutWithMock(lettuce, 'Feature')
    mox.StubOutWithMock(lettuce, '_import')

    lettuce._import('terrain')

    lettuce.fs.FeatureLoader('some_basepath').AndReturn(loader_mock)

    lettuce.sys.path.insert(0, 'some_basepath')
    lettuce.sys.path.remove('some_basepath')

    loader_mock.find_and_load_step_definitions()
    loader_mock.find_feature_files().AndReturn(['some_basepath/foo.feature'])
    lettuce.Feature.from_file('some_basepath/foo.feature'). \
        AndReturn(Feature.from_string(FEATURE2))

    mox.ReplayAll()

    runner = lettuce.Runner('some_basepath')
    CALLBACK_REGISTRY.clear()
    @before.all
    def set_state_to_before():
        world.all_steps.append('before')

    @step('append "during" to states')
    def append_during_to_all_steps(step):
        world.all_steps.append("during")

    @after.all
    def set_state_to_after(total):
        world.all_steps.append('after')
        isinstance(total, TotalResult)

    runner.run()

    mox.VerifyAll()

    assert_equals(
        world.all_steps,
        ['before', 'during', 'during', 'after']
    )

    mox.UnsetStubs()
