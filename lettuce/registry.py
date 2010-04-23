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

STEP_REGISTRY = {}
world = threading.local()
world._set = False

class CallbackDict(dict):
    def append_to(self, where, when, function):
        if function not in self[where][when]:
            self[where][when].append(function)

    def clear(self):
        for action_dict in self.values():
            for callback_list in action_dict.values():
                while callback_list:
                    callback_list.pop()


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
            'after_each': []
        },
        'feature': {
            'before_each': [],
            'after_each': []
        }
    }
)
