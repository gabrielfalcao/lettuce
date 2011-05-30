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

import string
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

def test_get_stripped_lines_ignore_comments():
    "strings.get_stripped_lines ignore lines that start with some char"
    my_string = '''

             first line

        # second line

    '''
    assert_equals(
        strings.get_stripped_lines(my_string, ignore_lines_starting_with="#"),
        [
            'first line',
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

def test_wise_startswith_also_strips_the_string():
    "strings.wise_startswith ignores case"
    assert strings.wise_startswith("  Gabriel", "g")
    assert strings.wise_startswith("  Gabriel", "G")
    assert strings.wise_startswith("  'Gabriel", "'")
    assert strings.wise_startswith("  #Gabriel", "#")
    assert strings.wise_startswith("  $Gabriel", "$")
    assert strings.wise_startswith("  ^Gabriel", "^")

def test_remove_it_accepts_regex_to_remove_all_from_string():
    "strings.remove_it accepts regex and remove all matches from string"
    assert_equals(
        strings.remove_it(u"Gabriel Falcão", u"[aã]"),
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
            'name': 'Miguel',
            'age': 19
        }

    ]

    assert_equals(
        strings.dicts_to_string(dicts, ['name', 'age']),
        u"| name           | age |\n"
        u"| Gabriel Falcão | 22  |\n"
        u"| Miguel         | 19  |\n"
    )

def test_dicts_to_string_escapes_pipe():
    "strings.dicts_to_string escapes pipe"

    dicts = [
        {
            'name': u'Gabriel | Falcão',
            'age': 22
        },
        {
            'name': 'Miguel | Arcanjo',
            'age': 19
        }

    ]

    assert_equals(
        strings.dicts_to_string(dicts, ['name', 'age']),
        u"| name             | age |\n"
        u"| Gabriel \\| Falcão | 22  |\n"
        u"| Miguel \\| Arcanjo | 19  |\n"
    )

def test_dicts_to_string_allows_empty():
    "strings.dicts_to_string allows empty"

    dicts = [
        {
            'name': u'Gabriel | Falcão',
            'age': 22
        },
        {
            'name': 'Miguel | Arcanjo'
        }
    ]
    assert_equals(
        strings.dicts_to_string(dicts, ['name', 'age']),
        u"| name             | age |\n"
        u"| Gabriel \\| Falcão | 22  |\n"
        u"| Miguel \\| Arcanjo |     |\n"
    )

def test_parse_hashes():
    "strings.parse_hashes"

    keys = [u'name', u'age']
    dicts = [
        {
            u'name': u'Gabriel Falcão',
            u'age': u'22'
        },
        {
            u'name': u'Miguel',
            u'age': u'33'
        }

    ]

    table = [
        u"| name           | age |\n",
        u"| Gabriel Falcão | 22  |\n",
        u"| Miguel         | 33  |\n",
    ]

    got_keys, got_dicts = strings.parse_hashes(table)

    assert_equals(keys, got_keys)
    assert_equals(dicts, got_dicts)

def test_parse_hashes_escapes_pipes():
    "strings.parse_hashes escapes pipe"

    keys = [u'name', u'age']
    dicts = [
        {
            u'name': u'Gabriel | Falcão',
            u'age': u'22'
        },
        {
            u'name': u'Miguel | Silva',
            u'age': u'33'
        }

    ]

    table = [
        u"| name              | age |\n",
        u"| Gabriel \| Falcão | 22  |\n",
        u"| Miguel \| Silva   | 33  |\n",
    ]

    got_keys, got_dicts = strings.parse_hashes(table)

    assert_equals(keys, got_keys)
    assert_equals(dicts, got_dicts)


def test_parse_hashes_allow_empty():
    "strings.parse_hashes allow empty"

    keys = [u'name', u'age']
    dicts = [
        {
            u'name': u'Gabriel',
            u'age': u'22'
        },
        {
            u'name': u'',
            u'age': u'33'
        },
        {
            u'name': u'Dave',
            u'age': u''
        }

    ]

    table = [
        u"| name    | age |\n",
        u"| Gabriel | 22  |\n",
        u"|         | 33  |\n",
        u"| Dave    |     |\n",
    ]

    got_keys, got_dicts = strings.parse_hashes(table)

    assert_equals(keys, got_keys)
    assert_equals(dicts, got_dicts)


def test_identifies_tag_lines():
    "strings.extract_tags_from_line not matching anything"
    # No tags tests
    tags = strings.extract_tags_from_line("")
    assert_equals(tags, None)
    tags = strings.extract_tags_from_line("normal line")
    assert_equals(tags, None)
    tags = strings.extract_tags_from_line("Scenario: line with name")
    assert_equals(tags, None)
    tags = strings.extract_tags_from_line(" | example step hash | line |")
    assert_equals(tags, None)
    tags = strings.extract_tags_from_line(
        " | example step hash | line @with | @tag like |")
    assert_equals(tags, None)


def test_finding_tags():
    "strings.extract_tags_from_line matching simple cases"

    tags = strings.extract_tags_from_line("@one")
    assert_equals(tags, ["one"])
    tags = strings.extract_tags_from_line("  @one  ")
    assert_equals(tags, ["one"])
    tags = strings.extract_tags_from_line("@one @two @three")
    assert_equals(tags, ["one", "two", "three"])
    tags = strings.extract_tags_from_line("  @one @two @three  ")
    assert_equals(tags, ["one", "two", "three"])
    tags = strings.extract_tags_from_line("  @one.two @three_four  ")
    assert_equals(tags, ["one.two", "three_four"])


def test_dont_find_tags_in_weird_cases():
    "don't find tags in weird cases"
    tags = strings.extract_tags_from_line("  @one two @three @four ")
    assert_equals(tags, None)



def test_consume_tag_lines():
    "strings.consume_tags_lines simple case"
    # No tags
    tags = []
    my_string = 'first line\n' \
        'second Line\n' \
        'third LIne\n' \
        'fourth lINe'
    lines = string.split(my_string, "\n")
    strings.consume_tags_lines(lines, tags)
    assert_equals(tags, [])
    assert_equals(len(lines), 4)
    # One line of tags
    tags = []
    my_string = '@tags @on\n' \
        'second Line\n' \
        'third LIne\n' \
        'fourth lINe'
    lines = string.split(my_string, "\n")
    strings.consume_tags_lines(lines, tags)
    assert_equals(tags, ["tags", "on"])
    assert_equals(len(lines), 3)   # first line gone
    assert_equals(lines[0], "second Line")
    # Two lines of tags
    tags = []
    my_string = '@tags @on\n' \
        '@second @line\n' \
        'third LIne\n' \
        'fourth lINe'
    lines = string.split(my_string, "\n")
    strings.consume_tags_lines(lines, tags)
    assert_equals(tags, ["tags", "on", "second", "line"])
    assert_equals(len(lines), 2)   # first two lines gone
    assert_equals(lines[0], "third LIne")
    # Only first line counts
    tags = []
    my_string = 'first line\n' \
        '@second @line\n' \
        'third LIne\n' \
        'fourth lINe'
    lines = string.split(my_string, "\n")
    strings.consume_tags_lines(lines, tags)
    assert_equals(tags, [])
    assert_equals(len(lines), 4)
    assert_equals(lines[0], "first line")
