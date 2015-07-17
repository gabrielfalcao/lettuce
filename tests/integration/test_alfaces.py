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
import os
import time
import commands
import multiprocessing

from tests.asserts import assert_equals, assert_not_equals
from lettuce.fs import FileSystem
current_directory = FileSystem.dirname(__file__)


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_django_agains_alfaces():
    'running the "harvest" django command with verbosity 3'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" in out
    assert "Test the django app FOO BAR" in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_django_background_server_running_in_background():
    'the django builtin server fails if the HTTP port is not available'

    import tornado.ioloop
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")
            raise SystemExit()

    def runserver():
        application = tornado.web.Application([
            (r"/", MainHandler),
        ])
        application.listen(8000)
        tornado.ioloop.IOLoop.instance().start()

    server = multiprocessing.Process(target=runserver)
    server.start()
    time.sleep(1)  # the child process take some time to get up

    e = 'Lettuce could not run the builtin Django server at 0.0.0.0:8000"\n' \
        'maybe you forgot a "runserver" instance running ?\n\n' \
        'well if you really do not want lettuce to run the server ' \
        'for you, then just run:\n\n' \
        'python manage.py --no-server'

    try:
        status, out = commands.getstatusoutput(
            "python manage.py harvest --verbosity=3 --no-color")
        assert_equals(out, e)
        assert_not_equals(status, 0)

    finally:
        os.kill(server.pid, 9)


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_django_background_server_running_in_background_with_custom_port():
    'the harvest command should take a --port argument'

    import tornado.ioloop
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")
            raise SystemExit()

    def runserver():
        application = tornado.web.Application([
            (r"/", MainHandler),
        ])
        application.listen(9889)
        tornado.ioloop.IOLoop.instance().start()

    server = multiprocessing.Process(target=runserver)
    server.start()
    time.sleep(1)  # the child process take some time to get up

    e = 'Lettuce could not run the builtin Django server at 0.0.0.0:9889"\n' \
        'maybe you forgot a "runserver" instance running ?\n\n' \
        'well if you really do not want lettuce to run the server ' \
        'for you, then just run:\n\n' \
        'python manage.py --no-server'

    try:
        status, out = commands.getstatusoutput(
            "python manage.py harvest --verbosity=3 --no-color --port=9889")
        assert_equals(out, e)
        assert_not_equals(status, 0)

    finally:
        os.kill(server.pid, 9)


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_limit_by_app_getting_all_apps_by_comma():
    'running "harvest" with --apps=multiple,apps,separated,by,comma'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color --apps=foobar,donothing")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" in out
    assert "Test the django app FOO BAR" in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_limit_by_app_getting_one_app():
    'running "harvest" with --apps=one_app'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color --apps=foobar")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" not in out
    assert "Test the django app FOO BAR" in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_excluding_apps_separated_by_comma():
    'running "harvest" with --avoid-apps=multiple,apps'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color --avoid-apps=donothing,foobar")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" not in out
    assert "Test the django app FOO BAR" not in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_excluding_app():
    'running "harvest" with --avoid-apps=one_app'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color --avoid-apps=donothing")
    assert_equals(status, 0, out)

    assert "Test the django app DO NOTHING" not in out
    assert "Test the django app FOO BAR" in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_running_only_apps_within_lettuce_apps_setting():
    'running the "harvest" will run only on configured apps if the ' \
             'setting LETTUCE_APPS is set'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --settings=onlyfoobarsettings --verbosity=3 --no-color")
    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" in out
    assert "Test the django app DO NOTHING" not in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_running_all_apps_but_lettuce_avoid_apps():
    'running the "harvest" will run all apps but those within ' \
             'LETTUCE_AVOID_APPS'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --settings=allbutfoobarsettings " \
        "--verbosity=3 --no-color")

    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" not in out
    assert "Test the django app DO NOTHING" in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_ignores_settings_avoid_apps_if_apps_argument_is_passed():
    'even if all apps are avoid in settings, it is possible to run a single ' \
          'app by --apps argument'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --settings=avoidallappssettings "
        "--verbosity=3 --no-color --apps=foobar,donothing")
    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" in out
    assert "Test the django app DO NOTHING" in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_no_server():
    '"harvest" --no-server does not start the server'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color --apps=foobar --no-server")

    assert_equals(status, 0, out)
    assert "Django's builtin server is running at" not in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_django_specifying_scenarios_to_run():
    'django harvest can run only specified scenarios with ' \
            '--scenarios or -s options'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color --scenarios=2,5 -a foobar")
    assert_equals(status, 0, out)

    assert "2nd scenario" in out
    assert "5th scenario" in out

    assert "1st scenario" not in out
    assert "3rd scenario" not in out
    assert "4th scenario" not in out
    assert "6th scenario" not in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_django_specifying_scenarios_to_run_by_tag():
    'django harvest can run only specified scenarios with ' \
            '--tags or -t options'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color --tag=fast -a foobar")
    assert_equals(status, 0, out)

    assert "3rd scenario" in out
    assert "6th scenario" in out

    assert "1st scenario" not in out
    assert "2rd scenario" not in out
    assert "4th scenario" not in out
    assert "5th scenario" not in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_running_only_specified_features():
    'it can run only the specified features, passing the file path'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color " \
        "foobar/features/foobar.feature")

    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" in out
    assert "Test the django app DO NOTHING" not in out


@FileSystem.in_directory(current_directory, 'django', 'alfaces')
def test_specifying_features_in_inner_directory():
    'it can run only the specified features from a subdirectory'

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=3 --no-color " \
        "foobar/features/deeper/deeper/leaf.feature")

    assert_equals(status, 0, out)

    assert "Test the django app FOO BAR" not in out
    assert "Test a feature in an inner directory" in out
    assert "Test the django app DO NOTHING" not in out
