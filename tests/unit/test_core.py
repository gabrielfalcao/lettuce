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
import os
from lettuce import core
from nose.tools import assert_equals
from nose.tools import assert_not_equals

def test_step_definition():
    "Step definition takes a function and a step, keeps its definition " \
    "relative path, and line + 1 (to consider the decorator)"

    def dumb():
        pass

    definition = core.StepDefinition("FOO BAR", dumb)
    assert_equals(definition.function, dumb)
    assert_equals(definition.file, os.path.relpath(__file__))
    assert_equals(definition.line, 27)

def test_step_description():
    "Step description takes a line and filename, and keeps the relative path for " \
    "filename"

    description = core.StepDescription(10, __file__)
    assert_equals(description.file, os.path.relpath(__file__))
    assert_not_equals(description.file, __file__)
    assert_equals(description.line, 10)

