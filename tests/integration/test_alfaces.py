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
from tests.asserts import assert_equals
from lettuce.fs import FileSystem

current_directory = FileSystem.dirname(__file__)

def test_django_agains_alfaces():
    'running the "harvest" django command with verbosity 3'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" in out
    assert "Test the django app FOO BAR" in out
    FileSystem.popd()

def test_limit_by_app_getting_all_apps_by_comma():
    'running "harvest" with --apps=multiple,apps,separated,by,comma'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3 --apps=foobar,donothing")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" in out
    assert "Test the django app FOO BAR" in out
    FileSystem.popd()

def test_limit_by_app_getting_one_app():
    'running "harvest" with --apps=one_app'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3 --apps=foobar")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" not in out
    assert "Test the django app FOO BAR" in out
    FileSystem.popd()

def test_excluding_apps_separated_by_comma():
    'running "harvest" with --avoid-apps=multiple,apps'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3 --avoid-apps=donothing,foobar")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" not in out
    assert "Test the django app FOO BAR" not in out
    FileSystem.popd()


def test_excluding_app():
    'running "harvest" with --avoid-apps=one_app'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3 --avoid-apps=donothing")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" not in out
    assert "Test the django app FOO BAR" in out
    FileSystem.popd()

def test_running_only_apps_within_lettuce_apps_setting():
    'running the "harvest" will run only on configured apps if the setting LETTUCE_APPS is set'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --settings=onlyfoobarsettings --verbosity=3")
    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" in out
    assert "Test the django app DO NOTHING" not in out
    FileSystem.popd()

def test_running_all_apps_but_lettuce_avoid_apps():
    'running the "harvest" will run all apps but those within LETTUCE_AVOID_APPS'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --settings=allbutfoobarsettings --verbosity=3")
    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" not in out
    assert "Test the django app DO NOTHING" in out
    FileSystem.popd()

def test_ignores_settings_avoid_apps_if_apps_argument_is_passed():
    'even if all apps are avoid in settings, it is possible to run a single app ' \
    'by --apps argument'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --settings=avoidallappssettings --verbosity=3 --apps=foobar,donothing")
    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" in out
    assert "Test the django app DO NOTHING" in out
    FileSystem.popd()


def test_no_server():
    '"harvest" --no-server does not start the server'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3 --apps=foobar --no-server")

    assert_equals(status, 0, out)
    assert "Django's builtin server is running at" not in out


def test_django_specifying_scenarios_to_run():
    'django harvest can run only specified scenarios with --scenarios or -s options'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3 --scenarios=2,5 -a foobar")
    assert_equals(status, 0, out)

    assert "2nd scenario" in out
    assert "5th scenario" in out

    assert "1st scenario" not in out
    assert "3rd scenario" not in out
    assert "4th scenario" not in out
    assert "6th scenario" not in out

    FileSystem.popd()

def test_running_only_specified_features():
    'it can run only the specified features, passing the file path'

    FileSystem.pushd(current_directory, "django", "alfaces")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3 foobar/features/foobar.feature")
    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" in out
    assert "Test the django app DO NOTHING" not in out
    FileSystem.popd()
