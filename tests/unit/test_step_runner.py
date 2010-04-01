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

from lettuce import step
from lettuce.core import Feature
from nose.tools import assert_raises
from nose.tools import assert_equals

FEATURE = """
Feature: Count steps ran
    Scenario: Total of steps ran
        Given I have a defined step
        When other step fails
        Then it won't reach here
"""

@step('I have a defined step')
def have_a_defined_step(*args, **kw):
    assert True

@step('other step fails')
def and_another():
    assert False, 'It should fail'

@step("it won't reach here")
def wont_reach_here():
    raise NotImplementedError('You should never reach here!')

def test_can_count_steps_and_its_states():
    "The scenario result has the steps passed, failed and skipped steps. " \
    "And total steps as well."

    f = Feature.from_string(FEATURE)
    feature_result = f.run()

    scenario_result = feature_result.scenario_results[0]
    assert_equals(len(scenario_result.steps_passed), 2)
    assert_equals(len(scenario_result.steps_failed), 1)
    assert_equals(len(scenario_result.steps_skipped), 1)
    assert_equals(scenario_result.total_steps, 3)
