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
# MERsteps.pyCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from lettuce import core
from lettuce import strings
from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.terrain import world


def wrt(what):
    if isinstance(what, unicode):
        what = what.encode('utf-8')
    sys.stdout.write(what)


@after.each_step
def print_step_running(step):
    if not step.display:
        return

    wrt(step.represent_string(step.original_sentence).rstrip())
    if not step.defined_at:
        wrt(" (undefined)")

    wrt('\n')
    if step.hashes:
        wrt(step.represent_hashes())

    if step.failed:
        print_spaced = lambda x: wrt("%s%s\n" % (" " * step.indentation, x))

        for line in step.why.traceback.splitlines():
            print_spaced(line)


@before.each_scenario
def print_scenario_running(scenario):
    if scenario.background:
        # Only print the background on the first scenario run
        # So, we determine if this was called previously with the attached background.
        # If so, skip the print_scenario() since we'll call it again in the after_background.
        if not hasattr(world, 'background_scenario_holder'):
            world.background_scenario_holder = {}
        if scenario.background not in world.background_scenario_holder:
            # We haven't seen this background before, add our 1st scenario
            world.background_scenario_holder[scenario.background] = scenario
            return
    wrt('\n')
    wrt(scenario.represented())


@before.each_background
def print_background_running(background):
    wrt('\n')
    wrt(background.represented())
    wrt('\n')


@after.each_background
def print_first_scenario_running(background, results):
    scenario = world.background_scenario_holder[background]
    print_scenario_running(scenario)


@after.outline
def print_outline(scenario, order, outline, reasons_to_fail):
    table = strings.dicts_to_string(scenario.outlines, scenario.keys)
    lines = table.splitlines()
    head = lines.pop(0)

    wline = lambda x: wrt("%s%s\n" % (" " * scenario.table_indentation, x))
    if order is 0:
        wrt("\n")
        wrt("%s%s:\n" % (" " * scenario.indentation, scenario.language.first_of_examples))
        wline(head)

    line = lines[order]
    wline(line)
    if reasons_to_fail:
        print_spaced = lambda x: wrt("%s%s\n" % (" " * scenario.table_indentation, x))
        elines = reasons_to_fail[0].traceback.splitlines()
        for line in elines:
            print_spaced(line)


@before.each_feature
def print_feature_running(feature):
    wrt("\n")
    wrt(feature.represented())

@after.harvest
@after.all
def print_end(total=None):
    wrt("\n")
    if isinstance(total, core.SummaryTotalResults):
        wrt("Test Suite Summary:\n")
        word = total.features_ran_overall > 1 and "features" or "feature"
        wrt("%d %s (%d passed)\n" % (
            total.features_ran_overall,
            word,
            total.features_passed_overall))
    else:
        word = total.features_ran > 1 and "features" or "feature"
        wrt("%d %s (%d passed)\n" % (
            total.features_ran,
            word,
            total.features_passed))

    word = total.scenarios_ran > 1 and "scenarios" or "scenario"
    wrt("%d %s (%d passed)\n" % (
        total.scenarios_ran,
        word,
        total.scenarios_passed))

    steps_details = []
    for kind in ("failed","skipped",  "undefined"):
        attr = 'steps_%s' % kind
        stotal = getattr(total, attr)
        if stotal:
            steps_details.append("%d %s" % (stotal, kind))

    steps_details.append("%d passed" % total.steps_passed)
    word = total.steps > 1 and "steps" or "step"
    wrt("%d %s (%s)\n" % (
        total.steps,
        word,
        ", ".join(steps_details)))

    if total.proposed_definitions:
        wrt("\nYou can implement step definitions for undefined steps with these snippets:\n\n")
        wrt("# -*- coding: utf-8 -*-\n")
        wrt("from lettuce import step\n\n")
        for step in total.proposed_definitions:
            method_name = step.proposed_method_name
            wrt("@step(u'%s')\n" % step.proposed_sentence)
            wrt("def %s:\n" % method_name)
            wrt("    assert False, 'This step must be implemented'\n")


    if total.failed_scenario_locations:
        # print list of failed scenarios, with their file and line number
        wrt("\nList of failed scenarios:\n")
        for scenario in total.failed_scenario_locations:
            wrt(scenario)
        wrt("\n")

def print_no_features_found(where):
    where = core.fs.relpath(where)
    if not where.startswith(os.sep):
        where = '.%s%s' % (os.sep, where)

    wrt('Oops!\n')
    wrt('could not find features at %s\n' % where)
