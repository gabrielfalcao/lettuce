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
#
# REMOVE THIS
import sys
import os
import lettuce
from StringIO import StringIO

from nose.tools import assert_equals, assert_true, with_setup
from sure import expect
from lettuce import registry
from lettuce import Runner
from lettuce import xunit_output
from lxml import etree
from tests.functional.test_runner import feature_name, bg_feature_name
from tests.asserts import prepare_stdout


def assert_xsd_valid(filename, content):
    # from nose.tools import set_trace; set_trace()

    xmlschema = etree.XMLSchema(etree.parse(
        open('/home/hackawaye/virtual_envs/lettuce_src/lettuce_ada/tests/functional/xunit.xsd')
    ))
    xmlschema.assertValid(etree.parse(StringIO(content)))


@with_setup(prepare_stdout, registry.clear)
def test_xunit_output_with_no_errors():
    'Test xunit output with no errors'
    # import pdb; pdb.set_trace()
    called = []

    def assert_correct_xml(filename, content):
        called.append(True)
        assert_xsd_valid(filename, content)
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
        assert_xsd_valid(filename, content)
        root = etree.fromstring(content)
        assert_equals(root.get("tests"), "2")
        assert_equals(root.get("failures"), "1")
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
        assert_xsd_valid(filename, content)
        assert_equals(filename, "custom_filename.xml")

    old = xunit_output.wrt_output
    xunit_output.wrt_output = assert_correct_xml
    runner = Runner(feature_name('error_traceback'), enable_xunit=True,
                    xunit_filename="custom_filename.xml")
    runner.run()

    assert_equals(1, len(called), "Function not called")
    xunit_output.wrt_output = old

@with_setup(prepare_stdout, registry.clear)
def test_xunit_output_with_unicode_characters_in_error_messages():
    called = []
    def assert_correct_xml(filename, content):
        called.append(True)
        assert_xsd_valid(filename, content)

    old = xunit_output.wrt_output
    xunit_output.wrt_output = assert_correct_xml
    runner = Runner(feature_name('unicode_traceback'), enable_xunit=True,
                    xunit_filename="custom_filename.xml")
    runner.run()

    assert_equals(1, len(called), "Function not called")
    xunit_output.wrt_output = old

@with_setup(prepare_stdout, registry.clear)
def test_xunit_does_not_throw_exception_when_missing_step_definition():
    def dummy_write(filename, content):
        pass

    old = xunit_output.wrt_output
    xunit_output.wrt_output = dummy_write
    runner = Runner(feature_name('missing_steps'), enable_xunit=True,
                    xunit_filename="mising_steps.xml")
    runner.run()

    xunit_output.wrt_output = old


@with_setup(prepare_stdout, registry.clear)
def test_xunit_output_with_no_steps():
    'Test xunit output with no steps'
    called = []
    def assert_correct_xml(filename, content):
        print filename
        print content
        called.append(True)
        assert_xsd_valid(filename, content)
        root = etree.fromstring(content)
        assert_equals(root.get("tests"), "1")
        assert_equals(root.find("testcase").get("name"), "Given I do nothing")
        assert_equals(len(root.getchildren()), 1)
        assert_equals(root.find("testcase/skipped").get("type"), "UndefinedStep(Given I do nothing)")
        assert_equals(float(root.find("testcase").get("time")), 0)

    old = xunit_output.wrt_output
    xunit_output.wrt_output = assert_correct_xml
    runner = Runner(feature_name('no_steps_defined'), enable_xunit=True)
    runner.run()

    assert_equals(1, len(called), "Function not called")
    xunit_output.wrt_output = old


@with_setup(prepare_stdout, registry.clear)
def test_xunit_output_with_background_section():
    'Test xunit output with a background section in the feature'
    called = []
    
    def assert_correct_xml(filename, content):
        called.append(True)
        assert_xsd_valid(filename, content)
        root = etree.fromstring(content)
        assert_equals(root.get("tests"), "1")
        assert_equals(root.get("failures"), "0")
        assert_equals(len(root.getchildren()), 2)

        passed1, passed2 = root.findall("testcase")
        assert_equals(passed1.get("name"), 'Given the variable "X" holds 2')
        assert_true(float(passed1.get("time")) > 0)
        assert_equals(passed2.get("name"), 'Given the variable "X" is equal to 2')
        assert_true(float(passed2.get("time")) > 0)
    
    from lettuce import step
    
    @step(ur'the variable "(\w+)" holds (\d+)')
    @step(ur'the variable "(\w+)" is equal to (\d+)')
    def just_pass(step, *args):
        pass
    
    filename = bg_feature_name('simple')
    old = xunit_output.wrt_output
    xunit_output.wrt_output = assert_correct_xml
    runner = Runner(filename, enable_xunit=True)
    runner.run()

    assert_equals(1, len(called), "Function not called")
    xunit_output.wrt_output = old


@with_setup(prepare_stdout, registry.clear)
def test_xunit_xml_output_with_no_errors():
    'Test xunit doc xml output'

    called = []

    def assert_correct_xml_output(filename, doc):
        called.append(True)
        expect(doc.toxml).when.called.doesnt.throw(UnicodeDecodeError)

    old = xunit_output.write_xml_doc
    xunit_output.write_xml_doc = assert_correct_xml_output
    runner = Runner(feature_name('xunit_unicode_and_bytestring_mixing'), enable_xunit=True)
    try:
        runner.run()
    finally:
        xunit_output.write_xml_doc = old
