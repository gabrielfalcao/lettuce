# -*- coding: utf-8 -*-
from lettuce import step

@step(u'Given I do nothing')
def given_i_do_nothing(step):
    pass

@step(u'Then I see that the test passes')
def then_i_see_that_the_test_passes(step):
    pass

@step(u'Then I should not see "([^"]+)"')
def then_should_not_see(step, email):
    pass

@step(u'Given some email addresses')
def given_email_addresses(step):
    pass
