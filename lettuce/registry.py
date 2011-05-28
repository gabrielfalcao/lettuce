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
import sys
import threading
import traceback

world = threading.local()
world._set = False

class CleanableDict(dict):
    def clear(self):
        for k in self.keys():
            del self[k]

class CallbackDict(CleanableDict):
    def _function_matches(self, one, other):
        params = 'co_filename', 'co_firstlineno'
        matches = list()

        for param in params:
            one_got = getattr(one.func_code, param)
            other_got = getattr(other.func_code, param)
            matches.append(one_got == other_got)

        return all(matches)

    def append_to(self, where, when, function):
        found = False

        for other_function in self[where][when]:
            if self._function_matches(other_function,function):
                found = True

        if not found:
            self[where][when].append(function)

    def clear(self):
        for name, action_dict in self.items():
            for callback_list in action_dict.values():
                while callback_list:
                    callback_list.pop()


STEP_REGISTRY = CleanableDict()
CALLBACK_REGISTRY = CallbackDict(
    {
        'all': {
            'before': list(),
            'after': list()
        },
        'step': {
            'before_each': list(),
            'after_each': list()
        },
        'scenario': {
            'before_each': list(),
            'after_each': list(),
            'outline': list()
        },
        'feature': {
            'before_each': list(),
            'after_each': list()
        },
        'app': {
            'before_each': list(),
            'after_each': list()
        },
        'harvest': {
            'before': list(),
            'after': list()
        },
        'handle_request': {
            'before': list(),
            'after': list()
        },
        'runserver': {
            'before': list(),
            'after': list()
        },
    }
)

def call_hook(situation, kind, *args, **kw):
    for callback in CALLBACK_REGISTRY[kind][situation]:
        try:
            callback(*args, **kw)
        except:
            traceback.print_exc()
            print
            sys.exit(2)

def clear():
    STEP_REGISTRY.clear()
    CALLBACK_REGISTRY.clear()
