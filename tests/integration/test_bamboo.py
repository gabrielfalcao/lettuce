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
from lettuce.fs import FileSystem
from nose.tools import assert_equals, assert_not_equals
from tests.util import run_scenario

current_directory = FileSystem.dirname(__file__)


@FileSystem.in_directory(current_directory, 'django', 'bamboo')
def test_mail_count():
    'Mail count is checked through Lettuce steps'

    status, out = run_scenario('leaves', 'count', 1)
    assert_equals(status, 0, out)
    status, out = run_scenario('leaves', 'count', 2)
    assert_equals(status, 0, out)

    status, out = run_scenario('leaves', 'count', 3)
    assert_not_equals(status, 0)
    assert "Length of outbox is 1" in out


@FileSystem.in_directory(current_directory, 'django', 'bamboo')
def test_mail_content():
    'Mail content is checked through Lettuce steps'

    status, out = run_scenario('leaves', 'content', 1)
    assert_equals(status, 0, out)
    status, out = run_scenario('leaves', 'content', 2)
    assert_equals(status, 0, out)

    status, out = run_scenario('leaves', 'content', 3)
    assert_not_equals(status, 0)
    assert "An email contained expected text in the body" in out


@FileSystem.in_directory(current_directory, 'django', 'bamboo')
def test_mail_fail():
    'Mock mail failure dies with error'

    status, out = run_scenario('leaves', 'mock-failure', 1)
    assert_not_equals(status, 0)
    assert "SMTPException: Failure mocked by lettuce" in out
