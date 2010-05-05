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

STEP1 = """
I have the following beverages in my freezer:
   | Name   | Type     | Price |
   | Skol   | Beer     |  3.80 |
   | Nestea | Ice-tea  |  2.10 |
"""

from lettuce.core import Step
from nose.tools import assert_equals

def test_step_has_repr():
    "Step implements __repr__ nicely"
    step = Step.from_string(STEP1)
    assert_equals(
        repr(step),
        '<Step: "I have the following beverages in my freezer:">'
    )

def test_can_get_sentence_from_string():
    "It should extract the sentence string from the whole step"

    step = Step.from_string(STEP1)

    assert isinstance(step, Step)

    assert_equals(
        step.sentence,
        "I have the following beverages in my freezer:"
    )

def test_can_parse_keys_from_table():
    "It should take the keys from the step, if it has a table"

    step = Step.from_string(STEP1)
    assert_equals(step.keys, ('Name', 'Type', 'Price'))

def test_can_parse_tables():
    "It should have a list of data from a given step, if it has a table"

    step = Step.from_string(STEP1)

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
