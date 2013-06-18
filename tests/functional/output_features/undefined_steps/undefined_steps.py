from lettuce import step, world

@step(u'this test step passes')
def this_test_step_passes(step):
    assert True

@step(u'(.*) squared is (.*)')
def val1_squared_is_val2(step, val1, val2):
    pass
