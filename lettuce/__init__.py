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

version = '0.1'
import sys
from lettuce.decorators import step
from lettuce.terrain import *
from lettuce.fs import FileSystem
#from lettuce.core import Feature

class Runner(object):
    def __init__(self, base_path):
        sys.path.insert(0, base_path)
        FileSystem.pushd(base_path)
        self.terrain = None
        try:
            self.terrain = __import__("terrain")
        except ImportError, e:
            if not "No module named terrain" in str(e):
                raise e

        sys.path.remove(base_path)
        FileSystem.popd()
