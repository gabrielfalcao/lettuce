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
# MERsteps.pyCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from lettuce import core
from lettuce.terrain import after
from lettuce.terrain import before

failed_scenarios = []
scenarios_and_its_fails = {}

def wrt(string):
    sys.stdout.write(string.encode('utf-8'))

@before.each_scenario
def print_scenario_running(scenario):
    wrt('%s ... ' % scenario.name)

@after.each_scenario
def print_scenario_ran(scenario):
    if scenario.passed:
        print "OK"
    elif scenario.failed:
        reason = scenarios_and_its_fails[scenario]
        if isinstance(reason.exception, AssertionError):
            print "FAILED"
        else:
            print "ERROR"

@after.each_step
def save_step_failed(step):
    if step.failed and step.scenario not in failed_scenarios:
        scenarios_and_its_fails[step.scenario] = step.why
        failed_scenarios.append(step.scenario)

@after.all
def print_end(total):
    if total.scenarios_passed < total.scenarios_ran:
        print # just a line to separate things here
        for scenario in failed_scenarios:
            reason = scenarios_and_its_fails[scenario]
            wrt(reason.traceback)

    wrt("\n")
    word = total.features_ran > 1 and "features" or "feature"
    wrt("%d %s (%d passed)\n" % (
        total.features_ran,
        word,
        total.features_passed
        )
    )

    word = total.scenarios_ran > 1 and "scenarios" or "scenario"
    wrt("%d %s (%d passed)\n" % (
        total.scenarios_ran,
        word,
        total.scenarios_passed
        )
    )

    steps_details = []
    for kind in ("failed","skipped",  "undefined"):
        attr = 'steps_%s' % kind
        stotal = getattr(total, attr)
        if stotal:
            steps_details.append(
                "%d %s" % (stotal, kind)
            )

    steps_details.append("%d passed" % total.steps_passed)
    word = total.steps > 1 and "steps" or "step"
    wrt("%d %s (%s)\n" % (
        total.steps,
        word,
        ", ".join(steps_details)
        )
    )

def print_no_features_found(where):
    where = core.fs.relpath(where)
    if not where.startswith(os.sep):
        where = '.%s%s' % (os.sep, where)

    wrt('Oops!\n')
    wrt(
        'could not find features at '
        '%s\n' % where
    )
