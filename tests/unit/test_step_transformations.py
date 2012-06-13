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
from lettuce import step, world, Feature
from sure import that, scenario

FEATURE1 = '''
Feature: Transformations
    Scenario: Simple matching
        Given the following users:
        | name    | email              |
        | Gabriel | gabriel@lettuce.it |
        | Lincoln | lincoln@comum.org  |
        When the user "Gabriel" is mentioned
        Then it becomes available in `world` as "last_user"
        And it is an `User` instance
'''

THIS_MODULE = sys.modules[__name__]


def step_runner_environ(context):
    "Make sure the test environment is what is expected"

    from lettuce import registry
    registry.clear()

    world.users = {}

    class User:
        def __init__(self, name, email):
            self.name = name
            self.email = email

        def save(self):
            world.users[self.name] = self

    @step('Given the following users')
    def collect_users(step):
        for data in step.hashes:
            user = User(**data)
            user.save()

    @step(r'When the user "(\w+)" is mentioned')
    def mention_user(step, user):
        world.last_user = user

    @step(r'Then it becomes available.* as "([\w_]+)"')
    def becomes_available(step, attribute):
        assert (hasattr(world, attribute),
                'world should contain the attribute %s' % attribute)

    @step(r'And it is an `(\w+)` instance')
    def and_is_instance_of(step, klass):
        import ipdb;ipdb.set_trace()
        assert that(world.last_user).is_a(klass)


@scenario(step_runner_environ)
def test_transformations(context):

    @step.caster(r'the user "(\w+)" is mentioned')
    def capture_users_by_name(name):
        return world.users[name]

    @step.caster(r'it is an `(\w+)`')
    def get_class_by_name(name):
        return THIS_MODULE[name]

    f = Feature.from_string(FEATURE1)
    feature_result = f.run()
    scenario_result = feature_result.scenario_results[0]

    assert that(scenario_result.steps_undefined).equals([])
    assert that(scenario_result.steps_failed).equals([])

    assert feature_result.passed
