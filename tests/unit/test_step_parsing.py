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

I_LIKE_VEGETABLES = "I hold a special love for green vegetables"
I_HAVE_TASTY_BEVERAGES = """I have the following tasty beverages in my freezer:
   | Name   | Type     | Price |
   | Skol   | Beer     |  3.80 |
   | Nestea | Ice-tea  |  2.10 |
"""
I_DIE_HAPPY = "I shall die with love in my heart"

from lettuce.core import Step
from nose.tools import assert_equals
from tests.asserts import *
import string

def test_step_has_repr():
    "Step implements __repr__ nicely"
    step = Step.from_string(I_HAVE_TASTY_BEVERAGES)
    assert_equals(
        repr(step),
        '<Step: "' + string.split(I_HAVE_TASTY_BEVERAGES, '\n')[0] + '">'
    )

def test_can_get_sentence_from_string():
    "It should extract the sentence string from the whole step"

    step = Step.from_string(I_HAVE_TASTY_BEVERAGES)

    assert isinstance(step, Step)

    assert_equals(
        step.sentence,
        string.split(I_HAVE_TASTY_BEVERAGES, '\n')[0]
    )

def test_can_parse_keys_from_table():
    "It should take the keys from the step, if it has a table"

    step = Step.from_string(I_HAVE_TASTY_BEVERAGES)
    assert_equals(step.keys, ('Name', 'Type', 'Price'))

def test_can_parse_tables():
    "It should have a list of data from a given step, if it has a table"

    step = Step.from_string(I_HAVE_TASTY_BEVERAGES)

    assert isinstance(step.hashes, list)
    assert_equals(len(step.hashes), 2)
    assert_equals(
        step.hashes[0],
        {
            'Name': 'Skol',
            'Type': 'Beer',
            'Price': '3.80'
        }
    )
    assert_equals(
        step.hashes[1],
        {
            'Name': 'Nestea',
            'Type': 'Ice-tea',
            'Price': '2.10'
        }
    )

def test_can_parse_a_unary_array_from_single_step():
    "It should extract a single ordinary step correctly into an array of steps"
    steps = Step.many_from_lines([I_HAVE_TASTY_BEVERAGES])
    assert_equals(len(steps), 1)
    assert isinstance(steps[0], Step)
    assert_equals(steps[0].sentence, string.split(I_HAVE_TASTY_BEVERAGES, '\n')[0])
    
def test_can_parse_a_unary_array_from_complicated_step():
    "It should extract a single tabular step correctly into an array of steps"
    steps = Step.many_from_lines([I_LIKE_VEGETABLES])
    assert_equals(len(steps), 1)
    assert isinstance(steps[0], Step)
    assert_equals(steps[0].sentence, I_LIKE_VEGETABLES)

def test_can_parse_regular_step_followed_by_tabular_step():
    "It should correctly extract two steps (one regular, one tabular) into an array."
    steps = Step.many_from_lines([I_LIKE_VEGETABLES, I_HAVE_TASTY_BEVERAGES])
    assert_equals(len(steps), 2)
    assert isinstance(steps[0], Step)
    assert isinstance(steps[1], Step)
    assert_equals(steps[0].sentence, I_LIKE_VEGETABLES)
    assert_equals(steps[1].sentence, string.split(I_HAVE_TASTY_BEVERAGES, '\n')[0])
    
def test_can_parse_tabular_step_followed_by_regular_step():
    "It should correctly extract two steps (one tabular, one regular) into an array."
    steps = Step.many_from_lines([I_HAVE_TASTY_BEVERAGES, I_LIKE_VEGETABLES])
    assert_equals(len(steps), 2)
    assert isinstance(steps[0], Step)
    assert isinstance(steps[1], Step)
    assert_equals(steps[0].sentence, string.split(I_HAVE_TASTY_BEVERAGES, '\n')[0])
    assert_equals(steps[1].sentence, I_LIKE_VEGETABLES)
    
def test_can_parse_two_ordinary_steps():
    "It should correctly extract two ordinary steps into an array."
    steps = Step.many_from_lines([I_DIE_HAPPY, I_LIKE_VEGETABLES])
    assert_equals(len(steps), 2)
    assert isinstance(steps[0], Step)
    assert isinstance(steps[1], Step)
    assert_equals(steps[0].sentence, I_DIE_HAPPY)
    assert_equals(steps[1].sentence, I_LIKE_VEGETABLES)
