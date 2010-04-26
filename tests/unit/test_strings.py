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

from nose.tools import assert_equals
from lettuce import strings

def test_escape_if_necessary_escapes_1_char():
    "strings.escape_if_necessary escapes regex if has only one char"
    assert_equals(strings.escape_if_necessary("$"), "[$]")
    assert_equals(strings.escape_if_necessary("^"), "[^]")
    assert_equals(strings.escape_if_necessary("#"), "[#]")
    assert_equals(strings.escape_if_necessary("("), "[(]")
    assert_equals(strings.escape_if_necessary(")"), "[)]")
    assert_equals(strings.escape_if_necessary("{"), "[{]")
    assert_equals(strings.escape_if_necessary("}"), "[}]")

def test_escape_if_necessary_escapes_nothing_if_has_more_than_1_char():
    "Escape if necessary does nothing if the string has more than 1 char"
    assert_equals(strings.escape_if_necessary("NOT ESCAPED"), "NOT ESCAPED")

def test_get_stripped_lines():
    "strings.get_stripped_lines strip every line, and jump empty ones"
    my_string = '''

             first line

       second line

    '''
    assert_equals(
        strings.get_stripped_lines(my_string),
        [
            'first line',
            'second line'
        ]
    )

def test_split_wisely_splits_ignoring_case():
    "strings.split_wisely splits ignoring case"
    my_string = 'first line\n' \
        'second Line\n' \
        'third LIne\n' \
        'fourth lINe\n'

    assert_equals(
        strings.split_wisely(my_string, 'line', strip=False),
        [
            'first ',
            'second ',
            'third ',
            'fourth '
        ]
    )

def test_split_wisely_splits_ignoring_case_and_stripping():
    "strings.split_wisely splits ignoring case and stripping"
    my_string = '''

             first line

       second Line

           third LIne
       fourth lINe

    '''
    assert_equals(
        strings.split_wisely(my_string, 'line', strip=True),
        [
            'first',
            'second',
            'third',
            'fourth'
        ]
    )

def test_wise_startswith_ignores_case():
    "strings.wise_startswith ignores case"
    assert strings.wise_startswith("Gabriel", "g")
    assert strings.wise_startswith("Gabriel", "G")
    assert strings.wise_startswith("'Gabriel", "'")
    assert strings.wise_startswith("#Gabriel", "#")
    assert strings.wise_startswith("$Gabriel", "$")
    assert strings.wise_startswith("^Gabriel", "^")

def test_remove_it_accepts_regex_to_remove_all_from_string():
    "strings.remove_it accepts regex and remove all matches from string"
    assert_equals(
        strings.remove_it("Gabriel Falcão", "[aã]"),
        "Gbriel Flco"
    )

def test_rfill_simple():
    "strings.rfill simple case"
    assert_equals(
        strings.rfill("ab", 10, "-"),
        "ab--------"
    )

def test_rfill_empty():
    "strings.rfill empty"
    assert_equals(
        strings.rfill("", 10, "*"),
        "**********"
    )

def test_rfill_blank():
    "strings.rfill blank"
    assert_equals(
        strings.rfill(" ", 10, "|"),
        " |||||||||"
    )

def test_rfill_full():
    "strings.rfill full"
    assert_equals(
        strings.rfill("abcdefghij", 10, "|"),
        "abcdefghij"
    )

def test_rfill_append():
    "strings.rfill append"
    assert_equals(
        strings.rfill("ab", 10, append="# path/to/file.extension: 2"),
        "ab        # path/to/file.extension: 2"
    )

def test_dicts_to_string():
    "strings.dicts_to_string"

    dicts = [
        {
            'name': u'Gabriel Falcão',
            'age': 22
        },
        {
            'name': 'Laryssa',
            'age': 19
        }

    ]

    assert_equals(
        strings.dicts_to_string(dicts, ['name', 'age']),
        "| name           | age |\n"
        "| Gabriel Falcão | 22  |\n"
        "| Laryssa        | 19  |\n"
    )

