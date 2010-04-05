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
from lettuce import fs
from lettuce.core import Feature

from lettuce.terrain import after
from lettuce.terrain import before

from lettuce.decorators import step
from lettuce.registry import CALLBACK_REGISTRY


def _import(name):
    return __import__(name)

class Runner(object):
    def __init__(self, base_path):
        sys.path.insert(0, base_path)
        fs.FileSystem.pushd(base_path)
        self.terrain = None
        self.loader = fs.FeatureLoader(base_path)
        try:
            self.terrain = _import("terrain")
        except ImportError, e:
            if not "No module named terrain" in str(e):
                raise e

        sys.path.remove(base_path)
        fs.FileSystem.popd()

    def run(self):
        for callback in CALLBACK_REGISTRY['all']['before']:
            callback()

        for filename in self.loader.find_feature_files():
            feature = Feature.from_file(filename)
            feature.run()

        for callback in CALLBACK_REGISTRY['all']['after']:
            callback()

