import sys

from lettuce import step

@step('When I write to stdout')
def write_stdout(step):
    print >> sys.stdout, "Badger"

@step('When I write to stderr')
def write_stderr(step):
    print >> sys.stderr, "Mushroom"

@step('Then I am happy')
def happy(step):
    pass
