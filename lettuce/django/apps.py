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

from os.path import join, dirname
from django.db.models import get_apps

def _filter_django_apps(module):
    "returns only those apps that are not builtin django.contrib"
    return not module.__name__.startswith("django.contrib")

def harvest_lettuces(path="features"):
    "gets all installed apps that are not from django.contrib"

    apps = filter(_filter_django_apps, get_apps())
    joinpath = lambda app: join(dirname(app.__file__), path)
    return map(joinpath, apps)
