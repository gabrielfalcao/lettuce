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


class Main(object):
    def __init__(self, callback):
        self.name = callback

    @classmethod
    def _add_method(cls, name, where, when):
        def method(self, fn):
            CALLBACK_REGISTRY.append_to(where, when % {'0': self.name}, fn)
            return fn

        method.__name__ = method.fn_name = name
        setattr(cls, name, method)

for name, where, when in (
        ('all', 'all', '%(0)s'),
        ('each_step', 'step', '%(0)s_each'),
        ('step_output', 'step',  '%(0)s_output'),
        ('each_scenario', 'scenario', '%(0)s_each'),
        ('each_background', 'background', '%(0)s_each'),
        ('each_feature', 'feature', '%(0)s_each'),
        ('harvest', 'harvest', '%(0)s'),
        ('each_app', 'app', '%(0)s_each'),
        ('runserver', 'runserver', '%(0)s'),
        ('handle_request', 'handle_request', '%(0)s'),
        ('outline', 'scenario', 'outline')):
    Main._add_method(name, where, when)

before = Main('before')
after = Main('after')
