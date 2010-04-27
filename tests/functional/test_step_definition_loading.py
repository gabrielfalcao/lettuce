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

from lettuce import Runner
from lettuce.terrain import before, world, after

def test_loads_sum_steps():
    "Can load step definitions from step_definitions folder"

    world.ran = False

    @before.each_step
    def assert_is_fine(step):
        world.ran = True

    runner = Runner(join(abspath(dirname(__file__)), 'simple_features', '2nd_feature_dir'), verbosity=0)
    runner.run()

    assert world.ran

def test_recursive_fallback():
    "If don't find a step_definitions folder, fallback loading all python " \
    "files under given dir, recursively."

    world.step_list = list()

    runner = Runner(join(abspath(dirname(__file__)), 'simple_features', '3rd_feature_dir'), verbosity=0)
    runner.run()

    assert_equals(
        world.step_list,
        [
            'Given I define step at look/here/step_one.py',
            'And at look/and_here/step_two.py',
            'Also at look/here/for_steps/step_three.py',
            'And finally at look/and_here/and_any_python_file/step_four.py',
        ]
    )

    del world.step_list
