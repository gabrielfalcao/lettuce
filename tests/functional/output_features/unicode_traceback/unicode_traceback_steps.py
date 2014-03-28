# -*- coding: utf-8 -*-
from lettuce import step

@step(u'my dæmi that passes')
def given_my_daemi_that_passes(step):
    pass

@step('my "(.*)" that blows an exception')
def given_my_daemi_that_blows_a_exception(step, name):
    assert False
