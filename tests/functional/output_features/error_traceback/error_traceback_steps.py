# -*- coding: utf-8 -*-
from lettuce import step

@step(u'Given my step that passes')
def given_my_step_that_passes(step):
    pass
    
@step(u'Given my step that blows a exception')
def given_my_step_that_blows_a_exception(step):
    raise RuntimeError