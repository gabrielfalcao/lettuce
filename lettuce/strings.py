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

import re
import time
import string

def escape_if_necessary(what):
    what = unicode(what)
    if len(what) is 1:
        what = u"[%s]" % what

    return what

def get_stripped_lines(string, ignore_lines_starting_with=''):
    string = unicode(string)
    lines = [unicode(l.strip()) for l in string.splitlines()]
    if ignore_lines_starting_with:
        filter_func = lambda x: x and not x.startswith(ignore_lines_starting_with)
    else:
        filter_func = lambda x: x

    lines = filter(filter_func, lines)

    return lines

def split_wisely(string, sep, strip=False):
    string = unicode(string)
    if strip:
        string=string.strip()
    else:
        string=string.strip("\n")
    sep = unicode(sep)

    regex = re.compile(escape_if_necessary(sep),  re.UNICODE | re.M | re.I)

    items = filter(lambda x: x, regex.split(string))
    if strip:
        items = [i.strip() for i in items]
    else:
        items = [i.strip("\n") for i in items]

    return [unicode(i) for i in items]

def wise_startswith(string, seed):
    string = unicode(string).strip()
    seed = unicode(seed)
    regex = u"^%s" % re.escape(seed)
    return bool(re.search(regex, string, re.I))

def remove_it(string, what):
    return unicode(re.sub(unicode(what), "", unicode(string)).strip())

def rfill(string, times, char=u" ", append=u""):
    string = unicode(string)
    missing = times - len(string)
    for x in range(missing):
        string += char

    return unicode(string) + unicode(append)

def getlen(string):
    return len(string) + 1

def dicts_to_string(dicts, order):
    escape = "#{%s}" % str(time.time())
    def enline(line):
        return unicode(line).replace("|", escape)
    def deline(line):
        return line.replace(escape, '\\|')

    keys_and_sizes = dict([(k, getlen(k)) for k in dicts[0].keys()])
    for key in keys_and_sizes:
        for data in dicts:
            current_size = keys_and_sizes[key]
            value = unicode(data.get(key, ''))
            size = getlen(value)
            if size > current_size:
                keys_and_sizes[key] = size

    names = []
    for key in order:
        size = keys_and_sizes[key]
        name = u" %s" % rfill(key, size)
        names.append(enline(name))

    table = [u"|%s|" % "|".join(names)]
    for data in dicts:
        names = []
        for key in order:
            value = data.get(key, '')
            size = keys_and_sizes[key]
            names.append(enline(u" %s" % rfill(value, size)))

        table.append(u"|%s|" % "|".join(names))

    return deline(u"\n".join(table) + u"\n")

def parse_hashes(lines):
    escape = "#{%s}" % str(time.time())
    def enline(line):
        return unicode(line.replace("\\|", escape)).strip()
    def deline(line):
        return line.replace(escape, '|')
    def discard_comments(lines):
        return [line for line in lines if not line.startswith('#')]

    lines = discard_comments(lines)
    lines = map(enline, lines)

    keys = []
    hashes = []
    if lines:
        first_line = lines.pop(0)
        keys = split_wisely(first_line, u"|", True)
        keys = map(deline, keys)

        for line in lines:
            values = split_wisely(line, u"|", True)
            values = map(deline, values)
            hashes.append(dict(zip(keys, values)))

    return keys, hashes

def parse_multiline(lines):
    multilines = []
    in_multiline = False
    for line in lines:
        if line == '"""':
            in_multiline = not in_multiline
        elif in_multiline:
            if line.startswith('"'):
                line = line[1:]
            if line.endswith('"'):
                line = line[:-1]
            multilines.append(line)
    return u'\n'.join(multilines)


def extract_tags_from_line(given_line):
    """returns tags_array if given_line contains tags, else None"""
    line = string.rstrip(given_line)
    tags = []
    if re.match("\s*?\@", line):
        tags = [tag for tag in re.split("\s*\@", line) if len(tag) > 0]
    if len(tags) == 0 or [tag for tag in tags if string.find(tag, " ") != -1]:
        return None
    return tags


def consume_tags_lines(lines, tags):
    """consumes lines from start of given set of lines and
       populates tags array,
       stops when run out of lines that are tag lines"""
    while True:
        line = lines[0]
        tags_on_lines = extract_tags_from_line(line)
        if tags_on_lines:
            tags.extend(tags_on_lines)
            lines.pop(0)
        else:
            break

def consume_scenario(lines, scenario_prefix):
    """return string of scenario text
       and reduce lines array by that much"""
    sep = unicode(scenario_prefix)
    regex = re.compile(escape_if_necessary(sep),  re.UNICODE | re.M | re.I)
    scenario_lines = []
    # Optional first lines are tags, is part of the scenario
    while len(lines) > 0:
        if extract_tags_from_line(lines[0]):
            scenario_lines.append(lines.pop(0))
        break
    # First line must be scenario_prefix
    if regex.match(lines[0]):
        scenario_lines.append(lines.pop(0))
    else:
        raise AssertionError("expecting scenario, at line [" + str(lines[0]) + "]")
    
    scenario_lines.extend(get_lines_till_next_scenario(lines, scenario_prefix))
    return unicode("\n".join(scenario_lines))

def get_lines_till_next_scenario(lines, scenario_prefix):
    """returns array of lines up till next scenario block"""
    sep = unicode(scenario_prefix)
    regex = re.compile(escape_if_necessary(sep),  re.UNICODE | re.M | re.I)
    scenario_lines = []
    in_multi_line_string = False
    # Scan till hit tags line or (next) scenario_prefix
    while len(lines) > 0:
        line = lines[0]
        if "\"\"\"" in line:
            in_multi_line_string = not in_multi_line_string
        if not in_multi_line_string:
            if regex.match(line) or extract_tags_from_line(line):
                break
        scenario_lines.append(lines.pop(0))
    return scenario_lines

def split_scenarios(lines, scenario_prefix):
    """returns array of strings, one per scenario"""
    scenario_strings = []
    while len(lines) > 0:
        scenario_string = consume_scenario(lines, scenario_prefix)
        if scenario_string:
            scenario_strings.append(scenario_string)
    return scenario_strings
