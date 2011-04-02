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
#
# REMOVE THIS
import sys
import os
import lettuce

from nose.tools import assert_equals, assert_true, with_setup
from lettuce import registry
from lettuce import Runner
from lettuce import xunit_output
from lxml import etree
from tests.functional.test_runner import feature_name
from tests.asserts import prepare_stdout

@with_setup(prepare_stdout, registry.clear)
def test_xunit_output_with_no_errors():
    'Test xunit output with no errors'
    called = []
    def assert_correct_xml(filename, content):
        called.append(True)
        root = etree.fromstring(content)
        assert_equals(root.get("tests"), "1")
        assert_equals(len(root.getchildren()), 1)
        assert_equals(root.find("testcase").get("name"), "Given I do nothing")
        assert_true(float(root.find("testcase").get("time")) > 0)

    old = xunit_output.wrt_output
    xunit_output.wrt_output = assert_correct_xml
    runner = Runner(feature_name('commented_feature'), enable_xunit=True)
    runner.run()

    assert_equals(1, len(called), "Function not called")
    xunit_output.wrt_output = old


@with_setup(prepare_stdout, registry.clear)
def test_xunit_output_with_one_error():
    'Test xunit output with one errors'
    called = []
    def assert_correct_xml(filename, content):
        called.append(True)
        root = etree.fromstring(content)
        assert_equals(root.get("tests"), "2")
        assert_equals(root.get("failed"), "1")
        assert_equals(len(root.getchildren()), 2)

        passed, failed = root.findall("testcase")
        assert_equals(passed.get("name"), "Given my step that passes")
        assert_true(float(passed.get("time")) > 0)
        assert_equals(failed.get("name"), "Given my step that blows a exception")
        assert_true(float(failed.get("time")) > 0)
        assert_true(failed.find("failure") is not None)

    old = xunit_output.wrt_output
    xunit_output.wrt_output = assert_correct_xml
    runner = Runner(feature_name('error_traceback'), enable_xunit=True)
    runner.run()

    assert_equals(1, len(called), "Function not called")
    xunit_output.wrt_output = old

@with_setup(prepare_stdout, registry.clear)
def test_xunit_output_with_different_filename():
    'Test xunit output with different filename'
    called = []
    def assert_correct_xml(filename, content):
        called.append(True)
        assert_equals(filename, "custom_filename.xml")

    old = xunit_output.wrt_output
    xunit_output.wrt_output = assert_correct_xml
    runner = Runner(feature_name('error_traceback'), enable_xunit=True,
                    xunit_filename="custom_filename.xml")
    runner.run()

    assert_equals(1, len(called), "Function not called")
    xunit_output.wrt_output = old


