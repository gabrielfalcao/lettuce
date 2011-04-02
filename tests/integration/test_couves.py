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
from lettuce.fs import FileSystem

current_directory = FileSystem.dirname(__file__)

def test_django_agains_couves():
    'it always call @after.all hooks, even after exceptions'

    FileSystem.pushd(current_directory, "django", "couves")

    status, out = commands.getstatusoutput("python manage.py harvest --verbosity=3")

    assert "Couves before all" in out
    assert "Couves after all" in out
    FileSystem.popd()

