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

import sys
from cStringIO import StringIO

from nose.tools import with_setup, assert_equal
from subunit.v2 import ByteStreamToStreamResult
from testtools import StreamToDict

from lettuce import Runner, registry
from lettuce.plugins import subunit_output
from tests.asserts import prepare_stdout
from tests.functional.test_runner import feature_name

class Includes(object):

    def __init__(self, d):
        self.d = d

    def __eq__(self, a):
        # for k, v in self.d.iteritems():
        #     assert_equal(v, a[k])
        return all((v == a[k] for k, v in self.d.iteritems()))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.d)


class Keys(object):

    def __init__(self, *keys):
        self.keys = keys

    def __eq__(self, a):
        return set(a.keys()) == set(self.keys)


class ContentContains(object):

    def __init__(self, text):
        self.text = text

    def __eq__(self, a):
        return self.text in a.as_text()

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.text)


class State(object):

    expect = []

    def handle_dict(self, test):
        try:
            d = self.expect.pop(0)
        except IndexError:
            raise AssertionError("Unexpected {}".format(test))

        assert_equal(d, test)

    def close_file(self, file_):
        """
        Close and check the file
        """

        file_.seek(0)
        case = ByteStreamToStreamResult(file_)
        result = StreamToDict(self.handle_dict)
        result.startTestRun()
        case.run(result)
        result.stopTestRun()

        file_.close()

    def setup(self):
        """
        Set up the for the test case
        """

        prepare_stdout()

        output = StringIO()
        self.patch = (subunit_output.open_file, subunit_output.close_file)

        subunit_output.open_file = lambda f: output
        subunit_output.close_file = self.close_file

    def teardown(self):
        """
        Tear down the test case
        """

        subunit_output.open_file, subunit_output.close_file = self.patch
        assert_equal(len(self.expect), 0, "Expected results left")

        registry.clear()

state = State()

@with_setup(state.setup, state.teardown)
def test_subunit_output_with_no_errors():
    """
    Test Subunit output with no errors
    """

    state.expect = [
        Includes({
            'id': 'one commented scenario: Do nothing',
            'status': 'success',
            'details': Keys('stdout', 'stderr'),
        }),
    ]

    runner = Runner(feature_name('commented_feature'), enable_subunit=True)
    runner.run()


@with_setup(state.setup, state.teardown)
def test_subunit_output_with_one_error():
    """
    Test Subunit output with one error
    """

    state.expect = [
        Includes({
            'status': 'success',
            'details': Keys('stdout', 'stderr'),
        }),
        Includes({
            'status': 'fail',
            'details': Keys('stdout', 'stderr', 'traceback'),
        }),
    ]

    runner = Runner(feature_name('error_traceback'), enable_subunit=True)
    runner.run()


@with_setup(state.setup, state.teardown)
def test_subunit_output_with_tags():
    """
    Test Subunit output with tags
    """

    state.expect = [
        Includes({
            'status': 'success',
            'tags': set(['slow-ish']),
        }),
        Includes({
            'status': 'success',
            'tags': set(['fast-ish']),
        }),
        Includes({
            'status': 'success',
            'tags': set(),
        }),
        Includes({
            'status': 'success',
            'tags': set(),
        }),
    ]

    runner = Runner(feature_name('tagged_features'), enable_subunit=True)
    runner.run()


@with_setup(state.setup, state.teardown)
def test_subunit_output_unicode():
    """
    Test Subunit output with unicode traceback
    """

    state.expect = [
        Includes({
            'status': 'success',
        }),
        Includes({
            'status': 'fail',
            'details': Includes({
                'traceback': ContentContains('given_my_daemi_that_blows_a_exception'),
            }),
        }),
    ]

    runner = Runner(feature_name('unicode_traceback'), enable_subunit=True)
    runner.run()


@with_setup(state.setup, state.teardown)
def test_subunit_output_console():
    """
    Test Subunit output to console
    """

    state.expect = [
        Includes({
            'status': 'success',
            'details': Includes({
                'stdout': ContentContains('Badger'),
            }),
        }),
        Includes({
            'status': 'success',
            'details': Includes({
                'stderr': ContentContains('Mushroom'),
            }),
        }),
    ]

    runner = Runner(feature_name('writes_to_console'), enable_subunit=True)
    runner.run()
