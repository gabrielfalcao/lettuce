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
import re
import sys

from lettuce import core
from lettuce import strings
from lettuce import terminal

from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.terrain import world


def wrt(what):
    if isinstance(what, unicode):
        what = what.encode('utf-8')
    sys.stdout.write(what)


def wrap_file_and_line(string, start, end):
    return re.sub(r'([#] [^:]+[:]\d+)', '%s\g<1>%s' % (start, end), string)


def wp(l):
    if l.startswith("\033[1;32m"):
        l = l.replace(" |", "\033[1;37m |\033[1;32m")
    if l.startswith("\033[1;36m"):
        l = l.replace(" |", "\033[1;37m |\033[1;36m")
    if l.startswith("\033[0;36m"):
        l = l.replace(" |", "\033[1;37m |\033[0;36m")
    if l.startswith("\033[0;31m"):
        l = l.replace(" |", "\033[1;37m |\033[0;31m")
    if l.startswith("\033[1;30m"):
        l = l.replace(" |", "\033[1;37m |\033[1;30m")
    if l.startswith("\033[1;31m"):
        l = l.replace(" |", "\033[1;37m |\033[0;31m")  
  
    return l


def write_out(what):
    wrt(wp(what))


@before.each_step
def print_step_running(step):
    if not step.defined_at or not step.display:
        return

    color = '\033[1;30m'

    if step.scenario and step.scenario.outlines:
        color = '\033[0;36m'

    string = step.represent_string(step.original_sentence)
    string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')
    write_out("%s%s" % (color, string))
    if step.hashes and step.defined_at:
        for line in step.represent_hashes().splitlines():
            write_out("\033[1;30m%s\033[0m\n" % line)


@after.each_step
def print_step_ran(step):
    if not step.display:
        return
    if step.scenario and step.scenario.outlines and (step.failed or step.passed or step.defined_at):
        return

    if step.hashes and step.defined_at:
        write_out("\033[A" * (len(step.hashes) + 1))

    string = step.represent_string(step.original_sentence)

    if not step.failed:
        string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')

    prefix = '\033[A'
    width, height = terminal.get_size()
    lines_up = len(string) / float(width)
    if lines_up < 1:
        lines_up = 1
    else:
        lines_up = int(lines_up) + 1

    #prefix = prefix * lines_up

    if step.failed:
        color = "\033[0;31m"
        string = wrap_file_and_line(string, '\033[1;41;33m', '\033[0m')

    elif step.passed:
        color = "\033[1;32m"

    elif step.defined_at:
        color = "\033[0;36m"

    else:
        color = "\033[0;33m"
        prefix = ""

    write_out("%s%s%s" % (prefix, color, string))

    if step.hashes:
        for line in step.represent_hashes().splitlines():
            write_out("%s%s\033[0m\n" % (color, line))

    if step.failed:
        wrt("\033[1;31m")
        pspaced = lambda x: wrt("%s%s" % (" " * step.indentation, x))
        lines = step.why.traceback.splitlines()

        for pindex, line in enumerate(lines):
            pspaced(line)
            if pindex + 1 < len(lines):
                wrt("\n")

        wrt("\033[0m\n")


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
    string = scenario.represented()
    string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')
    write_out("\n\033[1;37m%s" % string)


@after.outline
def print_outline(scenario, order, outline, reasons_to_fail):
    table = strings.dicts_to_string(scenario.outlines, scenario.keys)
    lines = table.splitlines()
    head = lines.pop(0)

    wline = lambda x: write_out("\033[0;36m%s%s\033[0m\n" % (" " * scenario.table_indentation, x))
    wline_success = lambda x: write_out("\033[1;32m%s%s\033[0m\n" % (" " * scenario.table_indentation, x))
    wline_red_outline = lambda x: write_out("\033[1;31m%s%s\033[0m\n" % (" " * scenario.table_indentation, x))
    wline_red = lambda x: write_out("%s%s" % (" " * scenario.table_indentation, x))
    if order is 0:
        wrt("\n")
        wrt("\033[1;37m%s%s:\033[0m\n" % (" " * scenario.indentation, scenario.language.first_of_examples))
        wline(head)

    line = lines[order]
    if reasons_to_fail:
        wline_red_outline(line)
    else:
        wline_success(line)
    if reasons_to_fail:
        elines = reasons_to_fail[0].traceback.splitlines()
        wrt("\033[1;31m")
        for pindex, line in enumerate(elines):
            wline_red(line)
            if pindex + 1 < len(elines):
                wrt("\n")

        wrt("\033[0m\n")


@before.each_feature
def print_feature_running(feature):
    string = feature.represented()
    lines = string.splitlines()

    write_out("\n")
    for line in lines:
        line = wrap_file_and_line(line, '\033[1;30m', '\033[0m')
        write_out("\033[1;37m%s\n" % line)

@after.harvest
@after.all
def print_end(total=None):
    if total is None:
        return
    write_out("\n")
    if isinstance(total, core.SummaryTotalResults):
        word = total.features_ran_overall > 1 and "features" or "feature"

        color = "\033[1;32m"
        if total.features_passed_overall is 0:
            color = "\033[0;31m"

        write_out("\033[1;37mTest Suite Summary:\n")
        write_out("\033[1;37m%d %s (%s%d passed\033[1;37m)\033[0m\n" % (
            total.features_ran_overall,
            word,
            color,
            total.features_passed_overall))

    else:
        word = total.features_ran > 1 and "features" or "feature"

        color = "\033[1;32m"
        if total.features_passed is 0:
            color = "\033[0;31m"

        write_out("\033[1;37m%d %s (%s%d passed\033[1;37m)\033[0m\n" % (
            total.features_ran,
            word,
            color,
            total.features_passed))

    color = "\033[1;32m"
    if total.scenarios_passed is 0:
        color = "\033[0;31m"

    word = total.scenarios_ran > 1 and "scenarios" or "scenario"
    write_out("\033[1;37m%d %s (%s%d passed\033[1;37m)\033[0m\n" % (
        total.scenarios_ran,
        word,
        color,
        total.scenarios_passed))

    steps_details = []
    kinds_and_colors = (
        ('failed', '\033[0;31m'),
        ('skipped', '\033[0;36m'),
        ('undefined', '\033[0;33m'),
    )

    for kind, color in kinds_and_colors:
        attr = 'steps_%s' % kind
        stotal = getattr(total, attr)
        if stotal:
            steps_details.append("%s%d %s" % (color, stotal, kind))

    steps_details.append("\033[1;32m%d passed\033[1;37m" % total.steps_passed)
    word = total.steps > 1 and "steps" or "step"
    content = "\033[1;37m, ".join(steps_details)

    word = total.steps > 1 and "steps" or "step"
    write_out("\033[1;37m%d %s (%s)\033[0m\n" % (
        total.steps,
        word,
        content))

    if total.proposed_definitions:
        wrt("\n\033[0;33mYou can implement step definitions for undefined steps with these snippets:\n\n")
        wrt("# -*- coding: utf-8 -*-\n")
        wrt("from lettuce import step\n\n")

        last = len(total.proposed_definitions) - 1
        for current, step in enumerate(total.proposed_definitions):
            method_name = step.proposed_method_name
            wrt("@step(u'%s')\n" % step.proposed_sentence)
            wrt("def %s:\n" % method_name)
            wrt("    assert False, 'This step must be implemented'")
            if current is last:
                wrt("\033[0m")

            wrt("\n")

    if total.failed_scenario_locations:
        # print list of failed scenarios, with their file and line number
        wrt("\n")
        wrt("\033[1;31m")
        wrt("List of failed scenarios:\n")
        wrt("\033[0;31m")
        for scenario in total.failed_scenario_locations:
            wrt(scenario)
        wrt("\033[0m")
        wrt("\n")


def print_no_features_found(where):
    where = core.fs.relpath(where)
    if not where.startswith(os.sep):
        where = '.%s%s' % (os.sep, where)

    write_out('\033[1;31mOops!\033[0m\n')
    write_out(
        '\033[1;37mcould not find features at '
        '\033[1;33m%s\033[0m\n' % where)


@before.each_background
def print_background_running(background):
    wrt('\n')
    wrt('\033[1;37m')
    wrt(background.represented())
    wrt('\033[0m\n')


@after.each_background
def print_first_scenario_running(background, results):
    scenario = world.background_scenario_holder[background]
    print_scenario_running(scenario)
