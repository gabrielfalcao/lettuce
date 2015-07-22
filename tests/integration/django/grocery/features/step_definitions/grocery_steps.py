# -*- coding: utf-8 -*-
import urllib2
from lettuce import step, before, world
from lettuce.django import django_url
from nose.tools import assert_equals
from django.conf import settings
from lxml import html as lhtml


@world.absorb
def get_url(url):
    if not url.startswith('http'):
        url = django_url(url)

    try:
        world.last_response = urllib2.urlopen(url)
    except Exception as e:
        world.last_response = e

    return world.last_response


@before.each_scenario
def prepare_the_world(scenario):
    world.statuses = []
    world.content_types = []
    world.last_response = None


@step(u'my settings.py has "(.*)" set to "(.*)"')
def given_my_settings_py_has_group1_set_to_group2(step, key, value):
    assert hasattr(settings, key), 'settings.%s is not set' % key
    assert_equals(getattr(settings, key), int(value))


@step(u'I see that requesting "(.*)" gets "(.*)"')
def then_i_see_that_requesting_group1_gets_group2(step, url, status):
    world.get_url(url)
    assert_equals(int(world.last_response.code), int(status))


@step(u'Given I fetch the urls:')
def given_i_fetch_the_urls(step):
    urls = map(lambda i: django_url(i['url']), step.hashes)
    for url in urls:
        http = world.get_url(url)
        world.statuses.append((url, http.code))
        world.content_types.append((url, http.headers.dict['content-type']))
        http.close()


@step(u'When all the responses have status code 200')
def when_all_the_responses_have_status_code_200(step):
    assert len(world.statuses) > 0, \
        "I can't check the status codes, it seems no requests were made"

    for url, status in world.statuses:
        assert status is 200, \
            "for %s the status code should be 200 but is %d" % (url, status)


@step(u'Then all the responses have mime type "(.*)"')
def then_all_the_responses_have_mime_type_group1(step, group1):
    for url, content_type in world.content_types:
        assert_equals(content_type, group1, 'failed at %s' % url)


@step(u'I navigate to "(.*)"')
def given_i_navigate_to_group1(step, url):
    world.get_url(url)


@step(u'try to resolve the assets provided by given HTML')
def when_i_try_to_resolve_the_assets_provided_by_given_html(step):
    dom = lhtml.fromstring(world.last_response.read())
    elements = dom.cssselect('link[href],script[src]')

    for e in elements:
        url = django_url(e.attrib.get('href', e.attrib.get('src')))
        http = world.get_url(url)
        world.statuses.append((url, http.code))
        world.content_types.append((url, http.headers.dict['content-type']))
        http.close()


@step(u'all the responses have are between one of those mime types:')
def then_all_the_responses_have_are_between_one_of_those_mime_types(step):
    expected_mimetypes = [d['mime-type'] for d in step.hashes]
    for url, content_type in world.content_types:
        assert content_type in expected_mimetypes, \
            'the url %s got an unexpected mimetype' % content_type


@step(u'should be an (\S+)')
def should_be_an_image(step, expected):
    got = world.last_response.headers['content-type']
    assert expected in got, \
        u'fetching the url %s, the content-type header should contain "%s", ' \
        'but it is actually %s' % (world.last_response.geturl(), expected, got)
