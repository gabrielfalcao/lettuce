# -*- coding: utf-8 -*-
from lettuce import before
from django.core.management import call_command


@before.harvest
def create_db(variables):
    call_command('syncdb', interactive=False, verbosity=0)
