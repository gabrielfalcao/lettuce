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
from lettuce.terrain import world
from lettuce import after

@step('I sum (\d+) and (\d+)')
def i_sum_x_and_y(step, x, y):
    world.sum = int(x) + int(y)

@step('it should result in (\d+)')
def it_should_result_in_z(step, z):
    assert_equals(world.sum, int(z))

@after.all
def clear_sum(total_results):
    if hasattr(world, 'sum'):
        del world.sum

