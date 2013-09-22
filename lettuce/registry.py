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
import os
import re
import threading
import traceback

from lettuce.exceptions import StepLoadingError

world = threading.local()
world._set = False


def _function_matches(one, other):
    return (os.path.abspath(one.func_code.co_filename) == os.path.abspath(other.func_code.co_filename) and
            one.func_code.co_firstlineno == other.func_code.co_firstlineno)


class CallbackDict(dict):
    def append_to(self, where, when, function):
        if not any(_function_matches(o, function) for o in self[where][when]):
            self[where][when].append(function)

    def clear(self):
        for name, action_dict in self.items():
            for callback_list in action_dict.values():
                callback_list[:] = []

class StepDict(dict):
    def load(self, step, func):
        self._assert_is_step(step, func)
        self[step] = func
        return func

    def load_func(self, func):
        regex = self._extract_sentence(func)
        return self.load(regex, func)

    def _extract_sentence(self, func):
        sentence = getattr(func, '__doc__', None)
        if sentence is None:
            sentence = func.func_name.replace('_', ' ')
            sentence = sentence[0].upper() + sentence[1:]
        return sentence

    def _assert_is_step(self, step, func):
        try:
            re.compile(step)
        except re.error, e:
            raise StepLoadingError("Error when trying to compile:\n"
                                   "  regex: %r\n"
                                   "  for function: %s\n"
                                   "  error: %s" % (step, func, e))




STEP_REGISTRY = StepDict()
CALLBACK_REGISTRY = CallbackDict(
    {
        'all': {
            'before': [],
            'after': [],
        },
        'step': {
            'before_each': [],
            'after_each': [],
        },
        'scenario': {
            'before_each': [],
            'after_each': [],
            'outline': [],
        },
        'background': {
            'before_each': [],
            'after_each': [],
        },
        'feature': {
            'before_each': [],
            'after_each': [],
        },
        'app': {
            'before_each': [],
            'after_each': [],
        },
        'harvest': {
            'before': [],
            'after': [],
        },
        'handle_request': {
            'before': [],
            'after': [],
        },
        'runserver': {
            'before': [],
            'after': [],
        },
    },
)


def call_hook(situation, kind, *args, **kw):
    for callback in CALLBACK_REGISTRY[kind][situation]:
        try:
            callback(*args, **kw)
        except Exception, e:
            print "=" * 1000
            traceback.print_exc(e)
            print
            raise


def clear():
    STEP_REGISTRY.clear()
    CALLBACK_REGISTRY.clear()
