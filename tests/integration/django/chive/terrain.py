# -*- coding: utf-8 -*-
from lettuce import before
from django.contrib.auth.models import User


@before.each_feature
def cause_exception(variables):
    User.objects.create_user(
        username='foo',
        password='bar',
    )
