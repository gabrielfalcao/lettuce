# -*- coding: utf-8 -*-
# <Lettuce - Behavior-driven design for python>
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

class Step(object):
    def __init__(self, sentence, remaining_lines):
        self.sentence = sentence
        keys, data_list = self._parse_remaining_lines(remaining_lines)

        self.keys = tuple(keys)
        self.data_list = list(data_list)

    def _parse_remaining_lines(self, lines):
        keys = []
        data_list = []
        if lines:
            keys = [k.strip() for k in lines.pop(0).split("|") if k]
            for line in lines:
                values = [k.strip() for k in line.split("|") if k]
                data_list.append(dict(zip(keys, values)))

        return keys, data_list

    @classmethod
    def from_string(cls, string):
        lines = strings.get_stripped_lines(string)
        sentence = lines.pop(0)
        return cls(sentence, remaining_lines=lines)

class Scenario(object):
    def __init__(self, name, remaining_lines):
        self.name = name
        self.steps = self._parse_remaining_lines(remaining_lines)

    def _parse_remaining_lines(self, lines):
        step_strings = []
        for line in lines:
            if line.strip().startswith("|"):
                step_strings[-1] += "\n%s" % line
            else:
                step_strings.append(line)

        return [Step.from_string(s) for s in step_strings]

    @classmethod
    def from_string(new_scenario, string):
        lines = strings.get_stripped_lines(string)
        scenario_line = lines.pop(0)
        line = scenario_line.replace("Scenario: ", "").strip()
        scenario =  new_scenario(name=line, remaining_lines=lines)
        return scenario

class Feature(object):
    def __init__(self, description, remaining_lines):
        self.description = description
        self.scenarios = self._parse_remaining_lines(remaining_lines)

    @classmethod
    def from_string(new_feature, string):
        lines = strings.get_stripped_lines(string)
        feature_line = lines.pop(0)
        line = feature_line.replace("Feature: ", "")
        feature = new_feature(description=line, remaining_lines=lines)
        return feature

    def _parse_remaining_lines(self, lines):
        scenarios = "\n".join(lines).split("Scenario: ")
        scenario_strings = ["Scenario: %s" % s for s in scenarios if s.strip()]
        return [Scenario.from_string(s) for s in scenario_strings]

