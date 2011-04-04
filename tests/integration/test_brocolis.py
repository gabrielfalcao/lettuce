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
import commands
from nose.tools import assert_equals
from lettuce.fs import FileSystem

current_directory = FileSystem.dirname(__file__)

def test_harvest_with_debug_mode_enabled():
    'python manage.py harvest -d turns settings.DEBUG=True'

    FileSystem.pushd(current_directory, "django", "brocolis")

    status, out = commands.getstatusoutput("python manage.py harvest -d leaves/features/enabled.feature")
    assert_equals(status, 0, out)
    status, out = commands.getstatusoutput("python manage.py harvest --debug-mode leaves/features/enabled.feature")
    assert_equals(status, 0, out)

    FileSystem.popd()

def test_harvest_with_debug_mode_disabled():
    'python manage.py harvest without turns settings.DEBUG=False'

    FileSystem.pushd(current_directory, "django", "brocolis")

    status, out = commands.getstatusoutput("python manage.py harvest leaves/features/disabled.feature")
    assert_equals(status, 0, out)

    FileSystem.popd()

def test_harvest_sets_environment_variabled_for_gae():
    'harvest sets environment variables SERVER_NAME and SERVER_PORT in order to work with google app engine'

    FileSystem.pushd(current_directory, "django", "brocolis")

    status, out = commands.getstatusoutput("python manage.py harvest leaves/features/appengine.feature")
    assert_equals(status, 0, out)

    FileSystem.popd()

