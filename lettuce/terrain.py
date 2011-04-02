# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2011>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from lettuce.registry import world
from lettuce.registry import CALLBACK_REGISTRY
world._set = True

def absorb(thing, name=None):
    if not isinstance(name, basestring):
        name = thing.__name__

    setattr(world, name, thing)
    return thing

world.absorb = absorb

@world.absorb
def spew(name):
    if hasattr(world, name):
        item = getattr(world, name)
        delattr(world, name)
        return item

class main(object):
    @classmethod
    def all(cls, function):
        CALLBACK_REGISTRY.append_to('all', cls.__name__, function)
        return function

    @classmethod
    def each_step(cls, function):
        CALLBACK_REGISTRY.append_to('step', "%s_each" % cls.__name__, function)
        return function

    @classmethod
    def each_scenario(cls, function):
        CALLBACK_REGISTRY.append_to('scenario', "%s_each" % cls.__name__, function)
        return function

    @classmethod
    def each_feature(cls, function):
        CALLBACK_REGISTRY.append_to('feature', "%s_each" % cls.__name__, function)
        return function

    @classmethod
    def harvest(cls, function):
        CALLBACK_REGISTRY.append_to('harvest', cls.__name__, function)
        return function

    @classmethod
    def each_app(cls, function):
        CALLBACK_REGISTRY.append_to('app', "%s_each" % cls.__name__, function)
        return function

    @classmethod
    def runserver(cls, function):
        CALLBACK_REGISTRY.append_to('runserver', cls.__name__, function)
        return function

    @classmethod
    def handle_request(cls, function):
        CALLBACK_REGISTRY.append_to('handle_request', cls.__name__, function)
        return function

    @classmethod
    def outline(cls, function):
        CALLBACK_REGISTRY.append_to('scenario', "outline", function)
        return function

class before(main):
    pass

class after(main):
    pass
