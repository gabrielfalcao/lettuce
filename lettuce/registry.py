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
import threading

world = threading.local()
world._set = False

class CleanableDict(dict):
    def clear(self):
        for k in self.keys():
            del self[k]

class CallbackDict(CleanableDict):
    def _function_matches(self, one, other):
        params = 'co_filename', 'co_firstlineno'
        matches = []

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
        for action_dict in self.values():
            for callback_list in action_dict.values():
                while callback_list:
                    callback_list.pop()


STEP_REGISTRY = CleanableDict()
CALLBACK_REGISTRY = CallbackDict(
    {
        'all': {
            'before': [],
            'after': []
        },
        'step': {
            'before_each': [],
            'after_each': []
        },
        'scenario': {
            'before_each': [],
            'after_each': [],
            'outline': []
        },
        'feature': {
            'before_each': [],
            'after_each': []
        }
    }
)

def clear():
    STEP_REGISTRY.clear()
    CALLBACK_REGISTRY.clear()
