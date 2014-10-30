# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
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
import sys
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


FEATURE3 = '''
Feature: Before and After callbacks all along lettuce
    @tag1
    Scenario: Before and After scenarios
        Given I append "during" to states

    @tag2
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
        ['before', 'during', 'after', 'before', 'during', 'after'],
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
        ['before', 'during', 'during', 'after'],
    )


def test_feature_hooks_not_invoked_if_no_scenarios_run():
    feature = Feature.from_string(FEATURE3)

    world.feature_steps = []
    feature.run(tags=['tag1'])
    assert_equals(
        world.feature_steps,
        ['before', 'during', 'after']
    )

    world.feature_steps = []
    feature.run(tags=['tag3'])
    assert_equals(
        world.feature_steps,
        []
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

    lettuce.fs.FeatureLoader('some_basepath', None).AndReturn(loader_mock)

    lettuce.sys.path.insert(0, 'some_basepath')
    lettuce.sys.path.remove('some_basepath')

    loader_mock.find_feature_files().AndReturn(['some_basepath/foo.feature'])
    loader_mock.find_and_load_step_definitions()
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
        ['before', 'during', 'during', 'after'],
    )

    mox.UnsetStubs()


def test_world_should_be_able_to_absorb_functions():
    u"world should be able to absorb functions"
    assert not hasattr(world, 'function1')

    @world.absorb
    def function1():
        return 'absorbed'

    assert hasattr(world, 'function1')
    assert callable(world.function1)

    assert_equals(world.function1(), 'absorbed')

    world.spew('function1')

    assert not hasattr(world, 'function1')


def test_world_should_be_able_to_absorb_lambdas():
    u"world should be able to absorb lambdas"
    assert not hasattr(world, 'named_func')

    world.absorb(lambda: 'absorbed', 'named_func')

    assert hasattr(world, 'named_func')
    assert callable(world.named_func)

    assert_equals(world.named_func(), 'absorbed')

    world.spew('named_func')

    assert not hasattr(world, 'named_func')


def test_world_should_be_able_to_absorb_classs():
   u"world should be able to absorb class"
   assert not hasattr(world, 'MyClass')

   if sys.version_info < (2, 6):
       return

   class MyClass:
       pass

   world.absorb(MyClass)

   assert hasattr(world, 'MyClass')
   assert_equals(world.MyClass, MyClass)

   assert isinstance(world.MyClass(), MyClass)

   world.spew('MyClass')

   assert not hasattr(world, 'MyClass')


def test_hooks_should_be_still_manually_callable():
    "terrain hooks should be still manually callable"

    @before.all
    def before_all():
        pass

    @before.harvest
    def before_harvest():
        pass

    @before.each_app
    def before_each_app():
        pass

    @before.each_step
    def before_each_step():
        pass

    @before.each_scenario
    def before_each_scenario():
        pass

    @before.each_feature
    def before_each_feature():
        pass

    @before.handle_request
    def before_handle_request():
        pass

    @before.outline
    def before_outline():
        pass

    @after.all
    def after_all():
        pass

    @after.harvest
    def after_harvest():
        pass

    @after.each_app
    def after_each_app():
        pass

    @after.each_step
    def after_each_step():
        pass

    @after.each_scenario
    def after_each_scenario():
        pass

    @after.each_feature
    def after_each_feature():
        pass

    @after.handle_request
    def after_handle_request():
        pass

    @after.outline
    def after_outline():
        pass

    assert callable(before_all), \
        '@before.all decorator should return the original function'

    assert callable(before_handle_request), \
        '@before.handle_request decorator should return the original function'

    assert callable(before_harvest), \
        '@before.harvest decorator should return the original function'

    assert callable(before_each_feature), \
        '@before.each_feature decorator should return the original function'

    assert callable(before_outline), \
        '@before.outline decorator should return the original function'

    assert callable(before_each_scenario), \
        '@before.each_scenario decorator should return the original function'

    assert callable(before_each_step), \
        '@before.each_step decorator should return the original function'

    assert callable(after_all), \
        '@after.all decorator should return the original function'

    assert callable(after_handle_request), \
        '@after.handle_request decorator should return the original function'

    assert callable(after_harvest), \
        '@after.harvest decorator should return the original function'

    assert callable(after_each_feature), \
        '@after.each_feature decorator should return the original function'

    assert callable(after_outline), \
        '@after.outline decorator should return the original function'

    assert callable(after_each_scenario), \
        '@after.each_scenario decorator should return the original function'

    assert callable(after_each_step), \
        '@after.each_step decorator should return the original function'
