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
import os
import re
import sys
import platform
import struct

from lettuce import strings
from lettuce import core
from lettuce.terrain import after
from lettuce.terrain import before

def get_terminal_size():
    if platform.system() == "Windows":
        return get_terminal_size_win()
    else:    
        return get_terminal_size_unix()

def get_terminal_size_win():
    #Windows specific imports
    from ctypes import windll, create_string_buffer
    # stdin handle is -10
    # stdout handle is -11
    # stderr handle is -12
    
    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
    else:
        sizex, sizey = 80, 25 # can't determine actual size - return default values
    
    return sizex, sizey


def get_terminal_size_unix():
    # Unix/Posix specific imports 
    import fcntl, termios
    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.getenv('LINES'), os.getenv('COLUMNS'))
        except:
            cr = (25, 80)

    return int(cr[1]), int(cr[0])


def wrt(what):
    sys.stdout.write(what.encode('utf-8'))

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

    return l

def write_out(what):
    wrt(wp(what))

@before.each_step
def print_step_running(step):
    if not step.defined_at:
        return

    color = '\033[1;30m'

    if step.scenario.outlines:
        color = '\033[0;36m'

    string = step.represent_string(step.original_sentence)
    string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')
    write_out("%s%s" % (color, string))
    if step.hashes:
        for line in step.represent_hashes().splitlines():
            write_out("\033[1;30m%s\033[0m\n" % line)

@after.each_step
def print_step_ran(step):
    if step.scenario.outlines:
        return

    if step.hashes:
        write_out("\033[A" * (len(step.hashes) + 1))

    string = step.represent_string(step.original_sentence)

    if not step.failed:
        string = wrap_file_and_line(string, '\033[1;30m', '\033[0m')


    prefix = '\033[A'
    width, height = get_terminal_size()
    lines_up = len(string) / float(width)
    if lines_up < 1:
        lines_up = 1
    else:
        lines_up = int(lines_up) + 1

    prefix = prefix * lines_up

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
    wline_red = lambda x: wrt("%s%s" % (" " * scenario.table_indentation, x))
    if order is 0:
        wrt("\n")
        wrt("\033[1;37m%s%s:\033[0m\n" % (" " * scenario.indentation, scenario.language.first_of_examples))
        wline(head)

    line = lines[order]
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

@after.all
def print_end(total):
    write_out("\n")

    word = total.features_ran > 1 and "features" or "feature"

    color = "\033[1;32m"
    if total.features_passed is 0:
        color = "\033[0;31m"

    write_out("\033[1;37m%d %s (%s%d passed\033[1;37m)\033[0m\n" % (
        total.features_ran,
        word,
        color,
        total.features_passed
        )
    )

    color = "\033[1;32m"
    if total.scenarios_passed is 0:
        color = "\033[0;31m"

    word = total.scenarios_ran > 1 and "scenarios" or "scenario"
    write_out("\033[1;37m%d %s (%s%d passed\033[1;37m)\033[0m\n" % (
        total.scenarios_ran,
        word,
        color,
        total.scenarios_passed
        )
    )

    steps_details = []
    kinds_and_colors = {
        'failed': '\033[0;31m',
        'skipped': '\033[0;36m',
        'undefined': '\033[0;33m'
    }


    for kind, color in kinds_and_colors.items():
        attr = 'steps_%s' % kind
        stotal = getattr(total, attr)
        if stotal:
            steps_details.append(
                "%s%d %s" % (color, stotal, kind)
            )

    steps_details.append("\033[1;32m%d passed\033[1;37m" % total.steps_passed)
    word = total.steps > 1 and "steps" or "step"
    content = "\033[1;37m, ".join(steps_details)

    word = total.steps > 1 and "steps" or "step"
    write_out("\033[1;37m%d %s (%s)\033[0m\n" % (
        total.steps,
        word,
        content
        )
    )

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

def print_no_features_found(where):
    where = core.fs.relpath(where)
    if not where.startswith(os.sep):
        where = '.%s%s' % (os.sep, where)

    write_out('\033[1;31mOops!\033[0m\n')
    write_out(
        '\033[1;37mcould not find features at '
        '\033[1;33m%s\033[0m\n' % where
    )
