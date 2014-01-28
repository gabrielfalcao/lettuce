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
import sys
import commands

from lettuce.fs import FileSystem
from tests.asserts import assert_not_equals

current_directory = FileSystem.dirname(__file__)
lib_directory = FileSystem.join(current_directory,  'lib')


OLD_PYTHONPATH = os.getenv('PYTHONPATH', ':'.join(sys.path))


def teardown():
    os.environ['PYTHONPATH'] = OLD_PYTHONPATH


@FileSystem.in_directory(current_directory, 'django', 'chive')
def test_django_admin_media_serving_on_django_13():
    'lettuce should serve admin static files properly on Django 1.3'

    os.environ['PYTHONPATH'] = "%s:%s" % (
        FileSystem.join(lib_directory, 'Django-1.3'),
        OLD_PYTHONPATH,
    )

    status, out = commands.getstatusoutput(
        "python manage.py harvest --verbosity=2 ./features/")

    assert_not_equals(status, 0)

    lines = out.splitlines()

    assert u"Preparing to serve django's admin site static files..." in lines
    assert u"Django's builtin server is running at 0.0.0.0:7000" in lines
