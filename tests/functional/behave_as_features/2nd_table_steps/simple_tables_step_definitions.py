# -*- coding: utf-8 -*-
from nose.tools import assert_equals
from lettuce import step, world, before

@before.each_scenario
def set_stack_and_result(scenario):
    world.stack = []
    world.result = 0

@step(u'I have entered (\d+) into the calculator')
def i_have_entered_NUM_into_the_calculator(step, num):
    world.stack.append(num)

@step(u'I press multiply')
def i_press_multiply(step):
    world.result = reduce(lambda x, y: x*y, map(int, world.stack))

@step(u'the result should be (\d+) on the screen')
def the_result_should_be_NUM_on_the_screen(step, num):
    assert_equals(world.result, int(num))

@step(u'I multiply (\d+) and (\d+) into the calculator')
def multiply_X_and_Y_into_the_calculator(step, x, y):
    step.behave_as('''
    Given I multiply these numbers:
      | number |
      | 55     |
      | 2      |
    '''.format(x, y))
@step(u'I multiply th[eo]se numbers')
def given_i_multiply_those_numbers(step):
    world.stack.extend(map(int, step.hashes.values_under('number')))
    world.result = reduce(lambda x, y: x*y, world.stack)
