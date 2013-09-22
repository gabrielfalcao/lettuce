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
from lettuce.registry import _function_matches, StepDict
from lettuce.exceptions import StepLoadingError

from nose.tools import assert_raises, assert_in, assert_equal


def test_function_matches_compares_with_abs_path():
    u"lettuce.registry._function_matches() should compare callback filenames with abspath"

    class fakecallback1:
        class func_code:
            co_filename = "/some/path/to/some/../file.py"
            co_firstlineno = 1

    class fakecallback2:
        class func_code:
            co_filename = "/some/path/to/file.py"
            co_firstlineno = 1

    assert _function_matches(fakecallback1, fakecallback2), \
        'the callbacks should have matched'

def test_StepDict_raise_StepLoadingError_if_load_first_argument_is_not_a_regex():
    u"lettuce.STEP_REGISTRY.load(step, func) should raise an error if step is not a regex"
    steps = StepDict()
    with assert_raises(StepLoadingError):
        steps.load("an invalid regex;)", lambda: "")

def test_StepDict_can_load_a_step_composed_of_a_regex_and_a_function():
    u"lettuce.STEP_REGISTRY.load(step, func) append item(step, func) to STEP_REGISTRY"
    steps = StepDict()
    func = lambda: ""
    step = "a step to test"
    steps.load(step, func)
    assert_in(step, steps)
    assert_equal(steps[step], func)

def test_StepDict_load_a_step_return_the_given_function():
    u"lettuce.STEP_REGISTRY.load(step, func) returns func"
    steps = StepDict()
    func = lambda: ""
    assert_equal(steps.load("another step", func), func)

def test_StepDict_can_extract_a_step_sentence_from_function_name():
    u"lettuce.STEP_REGISTRY._extract_sentence(func) parse func name and return a sentence"
    steps = StepDict()
    def a_step_sentence():
        pass
    assert_equal("A step sentence", steps._extract_sentence(a_step_sentence))

def test_StepDict_can_extract_a_step_sentence_from_function_doc():
    u"lettuce.STEP_REGISTRY._extract_sentence(func) parse func doc and return a sentence"
    steps = StepDict()
    def a_step_func():
        """A step sentence"""
        pass
    assert_equal("A step sentence", steps._extract_sentence(a_step_func))

def test_StepDict_can_load_a_step_from_a_function():
    u"lettuce.STEP_REGISTRY.load(step, func) append item(step, func) to STEP_REGISTRY"
    steps = StepDict()
    def a_step_to_test():
        pass

    steps.load_func(a_step_to_test)

    expected_sentence = "A step to test"
    assert_in(expected_sentence, steps)
    assert_equal(steps[expected_sentence], a_step_to_test)
