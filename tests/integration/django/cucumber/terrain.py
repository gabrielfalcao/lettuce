#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lettuce import before, after
from lettuce.django.server import ThreadedServer
from django.core.servers.basehttp import WSGIServer
from nose.tools import assert_equals

@before.harvest
def before_harvest(variables):
    assert_equals(variables.keys(), [
        'paths',
        'failed',
        'run_server',
        'verbosity',
        'args',
        'self',
        'apps_to_run',
        'apps_to_avoid',
        'options'
        ]
    )
    print "before harvest"
@after.harvest
def after_harvest(results):
    assert_equals(len(results), 2)
    assert_equals(results[0].steps_passed, 1)
    assert_equals(results[1].steps_passed, 1)
    print "after harvest"

@before.each_app
def before_app(module):
    assert module.__name__ in [
        'first',
        'second',
    ], '%r should be one of these app modules: "first", "seconds"' % module
    print "before each app"

@after.each_app
def after_app(module, result):
    assert module.__name__ in [
        'first',
        'second',
    ], '%r should be one of these app modules: "first", "seconds"' % module

    assert_equals(result.steps_passed, 1)
    print "after each app"

@before.runserver
def before_runserver(server):
    assert isinstance(server, ThreadedServer), '%s should be an instance of lettuce.django.server.ThreadedServer' % server
    assert_equals(server.address, '0.0.0.0')
    assert_equals(server.port, 8000)
    print "before within runserver"

@after.runserver
def after_runserver(server):
    assert isinstance(server, ThreadedServer), '%r should be an instance of lettuce.django.server.ThreadedServer' % server
    assert_equals(server.address, '0.0.0.0')
    assert_equals(server.port, 8000)
    print "after within runserver"

@before.handle_request
def before_handle_request(httpd, server):
    assert isinstance(httpd, WSGIServer), '%r should be an instance of WSGIServer' % server
    assert isinstance(server, ThreadedServer), '%r should be an instance of lettuce.django.server.ThreadedServer' % server
    print "before within handle_request"

@after.handle_request
def after_handle_request(httpd, server):
    assert isinstance(httpd, WSGIServer), '%r should be an instance of WSGIServer' % server
    assert isinstance(server, ThreadedServer), '%r should be an instance of lettuce.django.server.ThreadedServer' % server
    print "after within handle_request"

