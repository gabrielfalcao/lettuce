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
import re
from lettuce import strings
from lettuce.exceptions import ReasonToFail
from lettuce.exceptions import NoDefinitionFound

STEP_REGISTRY = {}

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

class StepDefinition(object):
    def __init__(self, function):
        self.function = function
        self.file = function.func_code.co_filename
        self.line = function.func_code.co_firstlineno + 1

    def __call__(self, *args, **kw):
        return self.function(*args, **kw)

class ScenarioDefinition(object):
    def __init__(self, scenario, filename, string):
        self.file = filename
        self.line = None

        for pline, part in enumerate(string.splitlines()):
            if re.search(re.escape(scenario.name), part):
                self.line = pline + 1
                break

class FeatureDefinition(object):
    def __init__(self, filename, lines):
        self.file = filename
        self.line = None
        for pline, part in enumerate(lines):
            if part.strip().startswith("Feature:"):
                self.line = pline + 2
                break

class Step(object):
    has_definition = False

    def __init__(self, sentence, remaining_lines):
        self.sentence = sentence
        self._remaining_lines = remaining_lines
        keys, data_list = self._parse_remaining_lines(remaining_lines)

        self.keys = tuple(keys)
        self.data_list = list(data_list)

    def __repr__(self):
        return u'<Step: "%s">' % self.sentence

    def _parse_remaining_lines(self, lines):
        return parse_data_list(lines)

    def _get_match(self, ignore_case):
        matched, func = None, lambda: None

        for regex, func in STEP_REGISTRY.items():
            matched = re.search(regex, self.sentence, ignore_case and re.I or 0)
            if matched:
                break

        return matched, StepDefinition(func)

    def run(self, ignore_case):
        matched, step_definition = self._get_match(ignore_case)

        if not matched:
            raise NoDefinitionFound(self)
        else:
            self.has_definition = True
            self.defined_at = step_definition
            try:
                step_definition()
            except Exception, e:
                self.why = ReasonToFail(e)
                raise

    @classmethod
    def from_string(cls, string):
        lines = strings.get_stripped_lines(string)
        sentence = lines.pop(0)
        return cls(sentence, remaining_lines=lines)

class Scenario(object):
    defined_at = None
    def __init__(self, name, remaining_lines, outlines):
        self.name = name
        self.steps = self._parse_remaining_lines(remaining_lines)
        self.outlines = outlines
        self.solved_steps = list(self._resolve_steps(self.steps, self.outlines))

    def __repr__(self):
        return u'<Scenario: "%s">' % self.name

    def run(self, ignore_case):
        steps_passed = []
        steps_failed = []
        steps_undefined = []

        for step in self.steps:
            try:
                step.run(ignore_case)
                steps_passed.append(step)
            except AssertionError:
                steps_passed.append(step)
                steps_failed.append(step)
                break
            except NoDefinitionFound, e:
                steps_undefined.append(e.step)
                continue

        skip = lambda x: x not in steps_passed and x not in steps_undefined
        steps_skipped = filter(skip, self.steps)

        return ScenarioResult(
            self,
            steps_passed,
            steps_failed,
            steps_skipped,
            steps_undefined
        )

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

    def _set_definition(self, definition):
        self.defined_at = definition

    @classmethod
    def from_string(new_scenario, string, with_file=None, original_string=None):
        splitted = strings.split_wisely(string, "Example[s]?[:]", True)
        string = splitted[0]

        outlines = []
        if len(splitted) is 2:
            part = splitted[1]
            keys, outlines = parse_data_list(strings.get_stripped_lines(part))

        lines = strings.get_stripped_lines(string)
        scenario_line = lines.pop(0)
        line = strings.remove_it(scenario_line, "Scenario( Outline)?: ")

        scenario =  new_scenario(name=line,
                                 remaining_lines=lines,
                                 outlines=outlines)

        if with_file and original_string:
            scenario_definition = ScenarioDefinition(scenario, with_file,
                                                     original_string)
            scenario._set_definition(scenario_definition)

        return scenario

class Feature(object):
    defined_at = None
    def __init__(self, name, remaining_lines, with_file, original_string):
        self.name = name
        self.scenarios, self.description = self._parse_remaining_lines(
            remaining_lines,
            original_string,
            with_file
        )

        self.original_string = original_string

        if with_file:
            feature_definition = FeatureDefinition(with_file, lines=remaining_lines)
            self._set_definition(feature_definition)

    def __repr__(self):
        return u'<Feature: "%s">' % self.name

    @classmethod
    def from_string(new_feature, string, with_file=None):
        lines = strings.get_stripped_lines(string)
        feature_line = lines.pop(0)
        line = feature_line.replace("Feature: ", "")
        feature = new_feature(name=line,
                              remaining_lines=lines,
                              with_file=with_file,
                              original_string=string)
        return feature

    @classmethod
    def from_file(new_feature, filename):
        f = open(filename)
        string = f.read()
        f.close()
        feature = new_feature.from_string(string, with_file=filename)
        return feature

    def _set_definition(self, definition):
        self.defined_at = definition

    def _parse_remaining_lines(self, lines, original_string, with_file=None):
        joined = "\n".join(lines)
        parts = strings.split_wisely(joined, "Scenario: ")
        description = ""

        if not strings.wise_startswith(joined, "Scenario:"):
            description = parts[0]
            parts.pop(0)

        scenario_strings = ["Scenario: %s" % s for s in parts if s.strip()]
        kw = dict(original_string=original_string, with_file=with_file)
        scenarios = [Scenario.from_string(s, **kw) for s in scenario_strings] # use filter here

        return scenarios, description

    def run(self, ignore_case=True):
        scenarios_ran = [scenario.run(ignore_case) for scenario in self.scenarios]
        return FeatureResult(self, *scenarios_ran)

class FeatureResult(object):
    def __init__(self, feature, *scenario_results):
        self.feature = feature
        self.scenario_results = scenario_results

class ScenarioResult(object):
    def __init__(self, scenario, steps_passed, steps_failed, steps_skipped,
                 steps_undefined):

        self.scenario = scenario

        self.steps_passed = steps_passed
        self.steps_failed = steps_failed
        self.steps_skipped = steps_skipped
        self.steps_undefined = steps_undefined

        all_lists = [steps_passed + steps_skipped + steps_undefined]
        self.total_steps = sum(map(len, all_lists))
