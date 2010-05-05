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
from lettuce import world
from lettuce.terrain import before
from nose.tools import assert_equals

@before.all
def set_balance():
    world.my_balance = 0

@step('I have (\d+) bucks')
def compare_bucks(step, cash):
    assert_equals(world.my_balance, int(cash))

@step('I have these items')
def havetheseitems(step):
    cars = {}
    for data in step.hashes:
        key = data['name']
        value = int(data['price'])
        cars[key] = value
    world.cars = cars


@step('sell the "([^"]+)"')
def sell_item(step, name):
    world.my_balance += world.cars[name]
    del world.cars[name]

@step('my garage contains:')
def alsothese(step):
    cars = {}
    for data in step.hashes:
        key = data['name']
        value = int(data['price'])
        cars[key] = value
    assert_equals(cars, world.cars)

