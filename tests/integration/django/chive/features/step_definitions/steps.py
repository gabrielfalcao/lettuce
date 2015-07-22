# -*- coding: utf-8 -*-
import urllib2
from nose.tools import assert_equals
from lettuce import step, world
from lettuce.django import django_url


@world.absorb
def get_url(url):
    if not url.startswith('http'):
        url = django_url(url)

    try:
        world.last_response = urllib2.urlopen(url)
    except Exception as e:
        world.last_response = e

    return world.last_response


@step(u'Given I go to "([^"]*)"')
def given_i_go_to_group1(step, url):
    world.get_url(url)


@step(u'Then I get a 404')
def then_i_get_a_404(step):
    assert_equals(world.last_response.code, 404)
