# -*- coding: utf-8 -*-
from lettuce import step

@step(u'a system-exiting error is raised')
def raise_system_exiting_error(step):
    raise KeyboardInterrupt
