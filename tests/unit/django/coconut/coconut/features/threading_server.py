# -*- coding: utf-8 -*-

import urllib
import time

from lettuce import step
from lettuce.django import django_url
from threading import Thread, activeCount
from nose.tools import *

class ThreadUrlVisit(Thread):
    def __init__(self, url):
        super(ThreadUrlVisit, self).__init__()
        
        self.url = django_url(url)
        self.start_time = None
        self.end_time = None
        
    def run(self):
        self.start_time = time.time()

        try:
            resp = urllib.urlopen(self.url)
            assert_equals(resp.read(), "OK")
        finally:
            self.end_time = time.time()

@step(u'Given I navigate to "([^"]*)" with (\d+) threads')
def given_i_navigate_to_group1_with_group2_threads(step, url, threads):
    step.scenario.started_threads = []
    step.scenario.start_threads = time.time()
    
    for i in xrange(int(threads)):
        thread = ThreadUrlVisit(url)
        step.scenario.started_threads.append(thread)
        thread.start()

@step(u'Then I see (\d+) threads in server execution')
def then_i_see_threads_in_server_execution(step, count):
    current_count = activeCount()
    assert_equals(str(current_count), count)
    
@step(u'Then I wait all requests')
def then_i_wait_all_requests(step):
    while activeCount() != 1:
        pass
    
    step.scenario.end_threads = time.time()
    

@step(u'Then all requests was finishing in pararell mode')
def then_all_requests_was_finishing_in_pararell_mode(step):
    end_times = [t.end_time for t in step.scenario.started_threads]

    max_time = max(end_times)
    min_time = min(end_times)
    total_time = max_time-min_time

    assert total_time < 20
