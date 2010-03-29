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
from lettuce import strings

def parse_data_list(lines):
    keys = []
    data_list = []
    if lines:
        first_line = lines.pop(0)
        keys = strings.split_wisely(first_line, "|", True)

        for line in lines:
            values = strings.split_wisely(line, "|", True)
            data_list.append(dict(zip(keys, values)))

    return keys, data_list

class Step(object):
    def __init__(self, sentence, remaining_lines):
        self.sentence = sentence
        self._remaining_lines = remaining_lines
        keys, data_list = self._parse_remaining_lines(remaining_lines)

        self.keys = tuple(keys)
        self.data_list = list(data_list)

    def _parse_remaining_lines(self, lines):
        return parse_data_list(lines)

    @classmethod
    def from_string(cls, string):
        lines = strings.get_stripped_lines(string)
        sentence = lines.pop(0)
        return cls(sentence, remaining_lines=lines)

class Scenario(object):
    def __init__(self, name, remaining_lines, outlines):
        self.name = name
        self.steps = self._parse_remaining_lines(remaining_lines)
        self.outlines = outlines
        self.solved_steps = list(self._resolve_steps(self.steps, self.outlines))

    def _resolve_steps(self, steps, outlines):
        for outline in outlines:
            for step in steps:
                sentence = step.sentence
                for k, v in outline.items():
                    sentence = sentence.replace(u'<%s>' % k, v)

                yield Step(sentence, step._remaining_lines)

    def _parse_remaining_lines(self, lines):
        step_strings = []
        for line in lines:
            if strings.wise_startswith(line, "|"):
                step_strings[-1] += "\n%s" % line
            else:
                step_strings.append(line)

        return [Step.from_string(s) for s in step_strings]

    @classmethod
    def from_string(new_scenario, string):
        splitted = strings.split_wisely(string, "Example[s]?[:]", True)
        string = splitted[0]

        outlines = []
        if len(splitted) is 2:
            part = splitted[1]
            keys, outlines = parse_data_list(strings.get_stripped_lines(part))

        lines = strings.get_stripped_lines(string)
        scenario_line = lines.pop(0)
        line = strings.remove_it(scenario_line, "Scenario( Outline)?: ")

        scenario =  new_scenario(name=line, remaining_lines=lines, outlines=outlines)

        return scenario

class Feature(object):
    def __init__(self, name, remaining_lines):
        self.name = name
        self.scenarios, self.description = self._parse_remaining_lines(
            remaining_lines
        )

    @classmethod
    def from_string(new_feature, string):
        lines = strings.get_stripped_lines(string)
        feature_line = lines.pop(0)
        line = feature_line.replace("Feature: ", "")
        feature = new_feature(name=line, remaining_lines=lines)
        return feature

    def _parse_remaining_lines(self, lines):
        joined = "\n".join(lines)
        parts = strings.split_wisely(joined, "Scenario: ")
        description = ""

        if not strings.wise_startswith(joined, "Scenario:"):
            description = parts[0]
            parts.pop(0)

        scenario_strings = ["Scenario: %s" % s for s in parts if s.strip()]
        scenarios = [Scenario.from_string(s) for s in scenario_strings]

        return scenarios, description

