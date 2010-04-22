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
release = 'barium'

import sys

from lettuce import fs
from lettuce.core import Feature, TotalResult

from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.terrain import world

from lettuce.decorators import step
from lettuce.registry import CALLBACK_REGISTRY

from couleur import Shell

__all__ = ['after', 'before', 'step', 'world']

def _import(name):
    return __import__(name)

class Runner(object):
    """ Main lettuce's test runner

    Takes a base path as parameter (string), so that it can look for
    features and step definitions on there.
    """
    def __init__(self, base_path, verbosity=4):
        """ lettuce.Runner will try to find a terrain.py file and
        import it from within `base_path`
        """
        sys.path.insert(0, base_path)
        self.terrain = None
        self.loader = fs.FeatureLoader(base_path)
        self.verbosity = verbosity
        try:
            self.terrain = _import("terrain")
        except Exception, e:
            if not "No module named terrain" in str(e):
                string = 'Lettuce has tried to load the conventional environment ' \
                    'module "terrain"\nbut it has errors, check its contents and ' \
                    'try to run lettuce again.\n'

                sys.stderr.write(string)
                raise SystemExit(1)

        sys.path.remove(base_path)

        if verbosity is 3:
            from lettuce.plugins import shell_output

        world._output = sys.stdout
        world._is_colored = verbosity is 4

    def run(self):
        """ Find and load step definitions, and them find and load
        features under `base_path` specified on constructor
        """
        self.loader.find_and_load_step_definitions()

        for callback in CALLBACK_REGISTRY['all']['before']:
            callback()

        results = []
        for filename in self.loader.find_feature_files():
            feature = Feature.from_file(filename)
            results.append(feature.run())

        for callback in CALLBACK_REGISTRY['all']['after']:
            callback()

        total = TotalResult(results)
        world._output.write("\n")

        world._output.write("%d feature (%d passed)\n" % (
            total.features_ran,
            total.features_passed
            )
        )

        world._output.write("%d scenario (%d passed)\n" % (
            total.scenarios_ran,
            total.scenarios_passed
            )
        )

        world._output.write("%d steps (%d passed)\n" % (
            total.steps,
            total.steps_passed
            )
        )
