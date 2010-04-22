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
import sys
from lettuce.terrain import after
from lettuce.terrain import before

@before.each_step
def print_step_running(step):
    sys.stdout.write(step.represent_string(step.sentence))

@after.each_step
def print_step_ran(step):
    sys.stdout.write("\033[A" + step.represent_string(step.sentence))

@before.each_scenario
def print_scenario_running(scenario):
    sys.stdout.write(scenario.represented())

@before.each_feature
def print_feature_running(feature):
    sys.stdout.write(feature.represented())
    sys.stdout.write("\n")

@after.all
def print_end(total):
    sys.stdout.write("\n")
    sys.stdout.write("%d feature (%d passed)\n" % (
        total.features_ran,
        total.features_passed
        )
    )

    sys.stdout.write("%d scenario (%d passed)\n" % (
        total.scenarios_ran,
        total.scenarios_passed
        )
    )

    sys.stdout.write("%d steps (%d passed)\n" % (
        total.steps,
        total.steps_passed
        )
    )
