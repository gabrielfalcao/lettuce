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
from os.path import dirname, abspath, join
from nose.tools import assert_equals

from lettuce import step
from lettuce import Runner
from lettuce.terrain import world
from lettuce.terrain import before, after

def test_imports_terrain_under_path_that_is_run():

    assert not hasattr(world, 'works_fine')

    runner = Runner(join(abspath(dirname(__file__)), 'simple_features', '1st_feature_dir'))
    assert runner.terrain
    assert hasattr(world, 'works_fine')
    assert world.works_fine

def test_after_each_all_is_executed_before_each_all():
    "terrain.before.each_all and terrain.after.each_all decorators"
    world.all_steps = []

    @before.all
    def set_state_to_before():
        world.all_steps.append('before')

    @step('append 1 in world all steps')
    def append_1_in_world_all_steps(step):
        world.all_steps.append("1")

    @step('append 2 more')
    def append_2_more(step):
        world.all_steps.append("2")

    @step('append 3 in world all steps')
    def append_during_to_all_steps(step):
        world.all_steps.append("3")

    @after.all
    def set_state_to_after(total):
        world.all_steps.append('after')

    runner = Runner(join(abspath(dirname(__file__)), 'simple_features', '2nd_feature_dir'))
    runner.run()

    assert_equals(
        world.all_steps,
        ['before', '1', '2', '3', 'after']
    )
