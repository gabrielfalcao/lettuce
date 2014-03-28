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
import re
import sys
from StringIO import StringIO
from nose.tools import assert_equals, assert_not_equals
from lettuce import registry
from difflib import Differ



def prepare_stdout():
    registry.clear()
    if isinstance(sys.stdout, StringIO):
        del sys.stdout
    std = StringIO()
    sys.stdout = std

def prepare_stderr():
    registry.clear()
    if isinstance(sys.stderr, StringIO):
        del sys.stderr
    std = StringIO()
    sys.stderr = std


def assert_lines(original, expected):
    original = original.decode('utf-8') if isinstance(original, basestring) else original
    assert_lines_unicode(original, expected)


def assert_lines_unicode(original, expected):
    if isinstance(expected, unicode):
        expected = expected.encode('utf-8')

    if isinstance(original, unicode):
        original = original.encode('utf-8')

    expected_lines = expected.splitlines(1)
    original_lines = original.splitlines(1)

    if original != expected:
        comparison = Differ().compare(expected_lines, original_lines)
        if isinstance(comparison, unicode):
            expected = expected.encode('utf-8')

        diff = u''.encode('utf-8').join(comparison)
        msg = (u'Output differed as follows:\n{0}\n'
               'Output was:\n{1}\nExpected was:\n{2}'.encode('utf-8'))

        raise AssertionError(repr(msg.format(diff, original, expected)).replace(r'\n', '\n'))

    assert_equals(
        len(expected), len(original),
        u'Output appears equal, but of different lengths.')


def assert_lines_with_traceback(one, other):
    lines_one = one.splitlines()
    lines_other = other.splitlines()
    regex = re.compile('File "([^"]+)", line \d+, in.*')

    error = '%r should be in traceback line %r.\nFull output was:\n' + one
    for line1, line2 in zip(lines_one, lines_other):
        if regex.search(line1) and regex.search(line2):
            found = regex.search(line2)

            filename = found.group(1)
            params = filename, line1
            assert filename in line1, error % params

        else:
            assert_unicode_equals(line1, line2)

    assert_unicode_equals(len(lines_one), len(lines_other))


def assert_unicode_equals(original, expected):
    if isinstance(original, basestring):
        original = original.decode('utf-8')
    assert_equals.im_class.maxDiff = None
    assert_equals(original, expected)

def assert_stderr(expected):
    string = sys.stderr.getvalue()
    assert_unicode_equals(string, expected)

def assert_stdout(expected):
    string = sys.stdout.getvalue()
    assert_unicode_equals(string, expected)

def assert_stdout_lines(other):
    assert_lines(sys.stdout.getvalue(), other)

def assert_stderr_lines(other):
    assert_lines(sys.stderr.getvalue(), other)

def assert_stdout_lines_with_traceback(other):
    assert_lines_with_traceback(sys.stdout.getvalue(), other)

def assert_stderr_lines_with_traceback(other):
    assert_lines_with_traceback(sys.stderr.getvalue(), other)
