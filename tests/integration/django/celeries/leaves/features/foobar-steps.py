from lettuce import step


@step(r'Given I say foo bar')
def given_i_say_foo_bar(step):
    pass


@step(r'Then it works')
def then_it_works(step):
    pass


@step(r'Then it fails')
def then_it_fails(step):
    assert False
