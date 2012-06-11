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
import logging
from lettuce import core
from lettuce.terrain import after
from lettuce.terrain import before


@before.each_step
def print_step_running(step):
    logging.info(step.represent_string(step.sentence))


@after.each_step
def print_step_ran(step):
    logging.info("\033[A" + step.represent_string(step.sentence))


@before.each_scenario
def print_scenario_running(scenario):
    logging.info(scenario.represented())


@before.each_feature
def print_feature_running(feature):
    logging.info("\n")
    logging.info(feature.represented())
    logging.info("\n")


@after.all
def print_end(total):
    logging.info("\n")
    word = total.features_ran > 1 and "features" or "feature"
    logging.info("%d %s (%d passed)\n" % (
        total.features_ran,
        word,
        total.features_passed))

    word = total.scenarios_ran > 1 and "scenarios" or "scenario"
    logging.info("%d %s (%d passed)\n" % (
        total.scenarios_ran,
        word,
        total.scenarios_passed))

    word = total.steps > 1 and "steps" or "step"
    logging.info("%d %s (%d passed)\n" % (
        total.steps,
        word,
        total.steps_passed))


def print_no_features_found(where):
    where = core.fs.relpath(where)
    if not where.startswith(os.sep):
        where = '.%s%s' % (os.sep, where)

    logging.info('\033[1;31mOops!\033[0m\n')
    logging.info(
        '\033[1;37mcould not find features at '
        '\033[1;33m%s\033[0m\n' % where)
