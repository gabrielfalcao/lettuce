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
import codecs
from copy import deepcopy
from lettuce import strings
from lettuce import languages
from lettuce.fs import FileSystem
from lettuce.registry import STEP_REGISTRY
from lettuce.registry import CALLBACK_REGISTRY
from lettuce.exceptions import ReasonToFail
from lettuce.exceptions import NoDefinitionFound
from lettuce.exceptions import LettuceSyntaxError

fs = FileSystem()

def parse_hashes(lines):
    lines = map(unicode, lines)
    keys = []
    hashes = []
    if lines:
        first_line = lines.pop(0)
        keys = strings.split_wisely(first_line, u"|", True)

        for line in lines:
            values = strings.split_wisely(line, u"|", True)
            hashes.append(dict(zip(keys, values)))

    return keys, hashes

class Language(object):
    code = 'en'
    name = 'English'
    native = 'English'
    feature = 'Feature'
    scenario = 'Scenario'
    examples = 'Examples|Scenarios'
    scenario_outline = 'Scenario Outline'
    scenario_separator = 'Scenario( Outline)?'
    def __init__(self, code=u'en'):
        self.code = code
        for attr, value in languages.LANGUAGES[code].items():
            setattr(self, attr, unicode(value))

    def __repr__(self):
        return '<Language "%s">' % self.code

    def __getattr__(self, attr):
        if not attr.startswith(u"first_of_"):
            return super(Language, self).__getattribute__(attr)

        name = re.sub(r'^first_of_', u'', attr)
        return unicode(getattr(self, name, u'').split(u"|")[0])

    @classmethod
    def guess_from_string(cls, string):
        match = re.search(u"language:[ ]*([^\s]+)", string)
        if match:
            instance = cls(match.group(1))
        else:
            instance = cls()

        return instance

class StepDefinition(object):
    """A step definition is a wrapper for user-defined callbacks. It
    gets a few metadata from file, such as filename and line number"""
    def __init__(self, step, function):
        self.function = function
        self.file = fs.relpath(function.func_code.co_filename)
        self.line = function.func_code.co_firstlineno + 1
        self.step = step

    def __call__(self, *args, **kw):
        """Method that actually wrapps the call to step definition
        callback. Sends step object as first argument
        """
        try:
            ret = self.function(self.step, *args, **kw)
            self.step.passed = True
        except Exception, e:
            self.step.failed = True
            self.step.why = ReasonToFail(e)
            raise e

        return ret

class StepDescription(object):
    """A simple object that holds filename and line number of a step
    description (step within feature file)"""
    def __init__(self, line, filename):
        self.file = filename
        if self.file:
            self.file = fs.relpath(self.file)

        self.line = line

class ScenarioDescription(object):
    """A simple object that holds filename and line number of a scenario
    description (scenario within feature file)"""

    def __init__(self, scenario, filename, string, language):
        self.file = fs.relpath(filename)
        self.line = None

        for pline, part in enumerate(string.splitlines()):
            part = part.strip()
            if re.match(u"%s: " % language.scenario_separator + re.escape(scenario.name), part):
                self.line = pline + 1
                break

class FeatureDescription(object):
    """A simple object that holds filename and line number of a feature
    description"""

    def __init__(self, feature, filename, string, language):
        lines = [l.strip() for l in string.splitlines()]
        self.file = fs.relpath(filename)
        self.line = None
        described_at = []
        description_lines = strings.get_stripped_lines(feature.description)
        for pline, part in enumerate(lines):
            part = part.strip()
            line = pline + 1
            if part.startswith(u"%s:" % language.first_of_feature):
                self.line = line
            else:
                for description in description_lines:
                    if part == description:
                        described_at.append(line)

        self.description_at = tuple(described_at)

class Step(object):
    """ Object that represents each step on feature files."""
    has_definition = False
    indentation = 4
    table_indentation = indentation + 2
    defined_at = None
    why = None
    ran = False
    passed = None
    failed = None
    related_outline = None

    def __init__(self, sentence, remaining_lines, line=None, filename=None):
        self.sentence = sentence
        self.original_sentence = sentence
        self._remaining_lines = remaining_lines
        keys, hashes = self._parse_remaining_lines(remaining_lines)

        self.keys = tuple(keys)
        self.hashes = list(hashes)
        self.described_at = StepDescription(line, filename)

        self.proposed_method_name, self.proposed_sentence = self.propose_definition()

    def propose_definition(self):

        sentence = unicode(self.original_sentence)
        method_name = sentence

        groups = [
            ('"', re.compile(r'("[^"]+")')), # double quotes
            ("'", re.compile(r"('[^']+')")), # single quotes
        ]

        matched = False
        attribute_names = []
        for char, group in groups:
            match_groups = group.search(self.original_sentence)

            if match_groups:
                matched = True
                for index, match in enumerate(group.findall(sentence)):
                    if char == "'":
                        char = re.escape(char)

                    sentence = sentence.replace(match, u'%s(.*)%s' % (char, char))
                    group_name = u"group%d" % (index + 1)
                    method_name = method_name.replace(match, group_name)
                    attribute_names.append(group_name)

        if not matched:
            sentence = re.escape(sentence).replace(r'\ ', ' ')

        method_name = '%s(step%s)' % (
            "_".join(re.findall("\w+", method_name)).lower(),
            attribute_names and (", %s" % ", ".join(attribute_names)) or ""
        )

        return method_name, sentence

    def solve_and_clone(self, data):
        sentence = self.sentence
        for k, v in data.items():
            sentence = sentence.replace(u'<%s>' % unicode(k), unicode(v))

        new = deepcopy(self)
        new.sentence = sentence
        return new

    def _calc_list_length(self, lst):
        length = self.table_indentation + 2
        for item in lst:
            length += len(item) + 2

        if len(lst) > 1:
            length += 1

        return length

    def _calc_key_length(self, data):
        return self._calc_list_length(data.keys())

    def _calc_value_length(self, data):
        return self._calc_list_length(data.values())

    @property
    def max_length(self):
        max_length_sentence = len(self.sentence) + self.indentation
        max_length_original = len(self.original_sentence) + self.indentation

        max_length = max([max_length_original, max_length_sentence])
        for data in self.hashes:
            key_size = self._calc_key_length(data)
            if key_size > max_length:
                max_length = key_size

            value_size = self._calc_value_length(data)
            if value_size > max_length:
                max_length = value_size

        return max_length

    def represent_string(self, string):
        head = ' ' * self.indentation + string
        where = self.described_at
        if self.defined_at:
            where = self.defined_at
        return strings.rfill(head, self.scenario.feature.max_length + 1, append=u'# %s:%d\n' % (where.file, where.line))

    def represent_hashes(self):
        lines = strings.dicts_to_string(self.hashes, self.keys).splitlines()
        return u"\n".join([(u" " * self.table_indentation) + line for line in lines]) + "\n"

    def __repr__(self):
        return u'<Step: "%s">' % self.sentence

    def _parse_remaining_lines(self, lines):
        return parse_hashes(lines)

    def _get_match(self, ignore_case):
        matched, func = None, lambda: None

        for regex, func in STEP_REGISTRY.items():
            matched = re.search(regex, self.sentence, ignore_case and re.I or 0)
            if matched:
                break

        return matched, StepDefinition(self, func)

    def pre_run(self, ignore_case, with_outline=None):
        matched, step_definition = self._get_match(ignore_case)
        self.related_outline = with_outline

        if not self.defined_at:
            if not matched:
                raise NoDefinitionFound(self)

            self.has_definition = True
            self.defined_at = step_definition

        return matched, step_definition

    def run(self, ignore_case):
        """Runs a step, trying to resolve it on available step
        definitions"""
        matched, step_definition = self.pre_run(ignore_case)
        self.ran = True
        kw = matched.groupdict()

        if kw:
            step_definition(**kw)
        else:
            groups = matched.groups()
            step_definition(*groups)

        self.passed = True
        return True

    @classmethod
    def from_string(cls, string, with_file=None, original_string=None):
        """Creates a new step from string"""
        lines = strings.get_stripped_lines(string)
        sentence = lines.pop(0)

        line = None
        if with_file and original_string:
            for pline, line in enumerate(original_string.splitlines()):
                if sentence in line:
                    line = pline + 1
                    break

        return cls(sentence, remaining_lines=lines, line=line, filename=with_file)

class Scenario(object):
    """ Object that represents each scenario on feature files."""
    described_at = None
    indentation = 2
    table_indentation = indentation + 2
    def __init__(self, name, remaining_lines, keys, outlines, with_file=None,
                 original_string=None, language=None):

        if not language:
            language = language()

        self.name = name
        self.language = language
        self.steps = self._parse_remaining_lines(remaining_lines,
                                                 with_file,
                                                 original_string)
        self.keys = keys
        self.outlines = outlines
        self.with_file = with_file
        self.original_string = original_string

        if with_file and original_string:
            scenario_definition = ScenarioDescription(self, with_file,
                                                      original_string,
                                                      language)
            self._set_definition(scenario_definition)

        self.solved_steps = list(self._resolve_steps(self.steps, self.outlines,
                                                     with_file, original_string))
        self._add_myself_to_steps()

    @property
    def max_length(self):
        if self.outlines:
            prefix = self.language.first_of_scenario_outline + ":"
        else:
            prefix = self.language.first_of_scenario + ":"

        max_length = len(u"%s %s" % (prefix, self.name)) + self.indentation

        for step in self.steps:
            if step.max_length > max_length:
                max_length = step.max_length

        for outline in self.outlines:
            key_size = self._calc_key_length(outline)
            if key_size > max_length:
                max_length = key_size

            value_size = self._calc_value_length(outline)
            if value_size > max_length:
                max_length = value_size

        return max_length

    def _calc_list_length(self, lst):
        length = self.table_indentation + 2
        for item in lst:
            length += len(item) + 2

        if len(lst) > 1:
            length += 2

        return length

    def _calc_key_length(self, data):
        return self._calc_list_length(data.keys())

    def _calc_value_length(self, data):
        return self._calc_list_length(data.values())

    def __repr__(self):
        return u'<Scenario: "%s">' % self.name

    @property
    def evaluated(self):
        for outline in self.outlines:
            steps = []
            for step in self.steps:
                new_step = step.solve_and_clone(outline)
                new_step.original_sentence = step.sentence
                new_step.scenario = self
                steps.append(new_step)

            yield (outline, steps)

    def run(self, ignore_case):
        """Runs a scenario, running each of its steps. Also call
        before_each and after_each callbacks for steps and scenario"""

        results = []
        for callback in CALLBACK_REGISTRY['scenario']['before_each']:
            callback(self)

        def run_scenario(almost_self, order=-1, outline=None, run_callbacks=False):
            all_steps = []
            steps_passed = []
            steps_failed = []
            steps_undefined = []

            reasons_to_fail = []
            for step in self.steps:
                if outline:
                    step = step.solve_and_clone(outline)

                try:
                    step.pre_run(ignore_case, with_outline=outline)

                    if run_callbacks:
                        for callback in CALLBACK_REGISTRY['step']['before_each']:
                            callback(step)

                    if not steps_failed and not steps_undefined:
                        step.run(ignore_case)
                        steps_passed.append(step)

                except AssertionError, e:
                    steps_failed.append(step)
                    reasons_to_fail.append(step.why)

                except NoDefinitionFound, e:
                    steps_undefined.append(e.step)

                finally:
                    all_steps.append(step)
                    if run_callbacks:
                        for callback in CALLBACK_REGISTRY['step']['after_each']:
                            callback(step)


            skip = lambda x: x not in steps_passed and x not in steps_undefined and x not in steps_failed

            steps_skipped = filter(skip, all_steps)
            if outline:
                for callback in CALLBACK_REGISTRY['scenario']['outline']:
                    callback(self, order, outline, reasons_to_fail)

            return ScenarioResult(
                self,
                steps_passed,
                steps_failed,
                steps_skipped,
                steps_undefined
            )

        if self.outlines:
            first = True
            for index, outline in enumerate(self.outlines):
                results.append(run_scenario(self, index, outline, run_callbacks=first))
                first = False
        else:
            results.append(run_scenario(self, run_callbacks=True))

        for callback in CALLBACK_REGISTRY['scenario']['after_each']:
            callback(self)

        return results

    def _add_myself_to_steps(self):
        for step in self.steps:
            step.scenario = self

        for step in self.solved_steps:
            step.scenario = self

    def _resolve_steps(self, steps, outlines, with_file, original_string):
        for outline in outlines:
            for step in steps:
                sentence = step.sentence
                for k, v in outline.items():
                    sentence = sentence.replace(u'<%s>' % k, v)

                yield Step(sentence, step._remaining_lines)

    def _parse_remaining_lines(self, lines, with_file, original_string):
        step_strings = []
        for line in lines:
            if strings.wise_startswith(line, u"|"):
                step_strings[-1] += "\n%s" % line
            else:
                step_strings.append(line)

        mkargs = lambda s: [s, with_file, original_string]
        return [Step.from_string(*mkargs(s)) for s in step_strings]

    def _set_definition(self, definition):
        self.described_at = definition

    def represented(self):
        make_prefix = lambda x: u"%s%s: " % (u' ' * self.indentation, x)
        if self.outlines:
            prefix = make_prefix(self.language.first_of_scenario_outline)
        else:
            prefix = make_prefix(self.language.first_of_scenario)

        head = prefix + self.name

        return strings.rfill(head, self.feature.max_length + 1, append=u'# %s:%d\n' % (self.described_at.file, self.described_at.line))

    def represent_examples(self):
        lines = strings.dicts_to_string(self.outlines, self.keys).splitlines()
        return "\n".join([(u" " * self.table_indentation) + line for line in lines]) + '\n'

    @classmethod
    def from_string(new_scenario, string, with_file=None, original_string=None, language=None):
        """ Creates a new scenario from string"""

        if not language:
            language = Language()

        splitted = strings.split_wisely(string, u"(%s):" % language.examples, True)
        string = splitted[0]
        keys = []
        outlines = []
        if len(splitted) > 1:
            part = splitted[-1]
            keys, outlines = parse_hashes(strings.get_stripped_lines(part))

        lines = strings.get_stripped_lines(string)
        scenario_line = lines.pop(0)

        for repl in (language.scenario_outline, language.scenario):
            scenario_line = strings.remove_it(scenario_line, u"(%s): " % repl)

        scenario = new_scenario(
            name=scenario_line,
            remaining_lines=lines,
            keys=keys,
            outlines=outlines,
            with_file=with_file,
            original_string=original_string,
            language=language
        )

        return scenario

class Feature(object):
    """ Object that represents a feature."""
    described_at = None
    def __init__(self, name, remaining_lines, with_file, original_string,
                 language=None):

        if not language:
            language = language()

        self.name = name
        self.language = language

        self.scenarios, self.description = self._parse_remaining_lines(
            remaining_lines,
            original_string,
            with_file
        )

        self.original_string = original_string

        if with_file:
            feature_definition = FeatureDescription(self,
                                                    with_file,
                                                    original_string,
                                                    language)
            self._set_definition(feature_definition)

        self._add_myself_to_scenarios()

    @property
    def max_length(self):
        max_length = len(u"%s: %s" % (self.language.first_of_feature, self.name))
        for line in self.description.splitlines():
            length = len(line.strip()) + Scenario.indentation
            if length > max_length:
                max_length = length

        for scenario in self.scenarios:
            if scenario.max_length > max_length:
                max_length = scenario.max_length

        return max_length

    def _add_myself_to_scenarios(self):
        for scenario in self.scenarios:
            scenario.feature = self

    def __repr__(self):
        return u'<%s: "%s">' % (self.language.first_of_feature, self.name)

    def get_head(self):
        return u"%s: %s" % (self.language.first_of_feature, self.name)

    def represented(self):
        length = self.max_length + 1

        filename = self.described_at.file
        line = self.described_at.line
        head = strings.rfill(self.get_head(), length, append=u"# %s:%d\n" % (filename, line))
        for description, line in zip(self.description.splitlines(), self.described_at.description_at):
            head += strings.rfill(u"  %s" % description, length, append=u"# %s:%d\n" % (filename, line))

        return head

    @classmethod
    def from_string(new_feature, string, with_file=None, language=None):
        """Creates a new feature from string"""
        lines = strings.get_stripped_lines(string)
        if not language:
            language = Language()

        found = len(re.findall(r'%s:[ ]*\w+' % language.feature, string))

        if found > 1:
            raise LettuceSyntaxError(
                with_file,
                'A feature file must contain ONLY ONE feature!'
            )

        elif found == 0:
            raise LettuceSyntaxError(
                with_file,
                'Features must have a name. e.g: "Feature: This is my name"'
            )


        while lines:
            matched = re.search(r'%s:(.*)' % language.feature, lines[0], re.I)
            if matched:
                name = matched.groups()[0].strip()
                break

            lines.pop(0)

        feature = new_feature(name=name,
                              remaining_lines=lines,
                              with_file=with_file,
                              original_string=string,
                              language=language)
        return feature

    @classmethod
    def from_file(new_feature, filename):
        """Creates a new feature from filename"""
        f = codecs.open(filename, "r", "utf-8")
        string = f.read()
        f.close()
        language = Language.guess_from_string(string)
        feature = new_feature.from_string(string, with_file=filename, language=language)
        return feature

    def _set_definition(self, definition):
        self.described_at = definition

    def _parse_remaining_lines(self, lines, original_string, with_file=None):

        joined = u"\n".join(lines[1:])

        # replacing occurrencies of Scenario Outline, with just "Scenario"
        scenario_prefix = u'%s:' % self.language.first_of_scenario
        regex = re.compile(u"%s:\s" % self.language.scenario_separator, re.U | re.I)
        joined = regex.sub(scenario_prefix, joined)

        parts = strings.split_wisely(joined, scenario_prefix)

        description = u""

        if not re.search("^" + scenario_prefix, joined):
            description = parts[0]
            parts.pop(0)

        scenario_strings = [
            u"%s: %s" % (self.language.first_of_scenario, s) for s in parts if s.strip()
        ]
        kw = dict(
            original_string=original_string,
            with_file=with_file,
            language=self.language
        )

        scenarios = [Scenario.from_string(s, **kw) for s in scenario_strings]

        return scenarios, description

    def run(self, ignore_case=True):
        for callback in CALLBACK_REGISTRY['feature']['before_each']:
            callback(self)

        scenarios_ran = []

        [scenarios_ran.extend(scenario.run(ignore_case)) for scenario in self.scenarios]

        for callback in CALLBACK_REGISTRY['feature']['after_each']:
            callback(self)

        return FeatureResult(self, *scenarios_ran)

class FeatureResult(object):
    """Object that holds results of each scenario ran from within a feature"""
    def __init__(self, feature, *scenario_results):
        self.feature = feature
        self.scenario_results = scenario_results

    @property
    def passed(self):
        return all([result.passed for result in self.scenario_results])

class ScenarioResult(object):
    """Object that holds results of each step ran from within a scenario"""
    def __init__(self, scenario, steps_passed, steps_failed, steps_skipped,
                 steps_undefined):

        self.scenario = scenario

        self.steps_passed = steps_passed
        self.steps_failed = steps_failed
        self.steps_skipped = steps_skipped
        self.steps_undefined = steps_undefined

        all_lists = [steps_passed + steps_skipped + steps_undefined + steps_failed]
        self.total_steps = sum(map(len, all_lists))

    @property
    def passed(self):
        return self.total_steps is len(self.steps_passed)

class TotalResult(object):
    def __init__(self, feature_results):
        self.feature_results = feature_results
        self.scenario_results = []
        self.steps_passed = 0
        self.steps_failed = 0
        self.steps_skipped = 0
        self.steps_undefined= 0
        self._proposed_definitions = []
        self.steps = 0
        for feature_result in self.feature_results:
            for scenario_result in feature_result.scenario_results:
                self.scenario_results.append(scenario_result)
                self.steps_passed += len(scenario_result.steps_passed)
                self.steps_failed += len(scenario_result.steps_failed)
                self.steps_skipped += len(scenario_result.steps_skipped)
                self.steps_undefined += len(scenario_result.steps_undefined)
                self.steps += scenario_result.total_steps
                self._proposed_definitions.extend(scenario_result.steps_undefined)


    def _filter_proposed_definitions(self):
        sentences = []
        for step in self._proposed_definitions:
            if step.proposed_sentence not in sentences:
                sentences.append(step.proposed_sentence)
                yield step

    @property
    def proposed_definitions(self):
        return list(self._filter_proposed_definitions())

    @property
    def features_ran(self):
        return len(self.feature_results)

    @property
    def features_passed(self):
        return len([result for result in self.feature_results if result.passed])

    @property
    def scenarios_ran(self):
        return len(self.scenario_results)

    @property
    def scenarios_passed(self):
        return len([result for result in self.scenario_results if result.passed])
