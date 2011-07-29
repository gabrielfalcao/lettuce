.. _recipes-nose:

Lettuce recipe: Using nose for pretty assertions
================================================

Lettuce uses python's builtin exception :exc:`AssertionError` to mark
tests as failed.

Although in order to describe the assertion with a custom string you
would need to do something like:

.. highlight:: python

::

    from lettuce import step

    @step('some step with "(.*)"'):
    def some_step(step, from):
        assert from == 'expectation', \
            "Ooops, '%s' should be equal 'expectation', but isn't" % from

nose_ is a python module that provides a set of assert functions that
already have a nice description, and fortunately it still uses
:exc:`AssertionError`, which makes nose_ totally compliant with
lettuce.

The example below shows how the step above could be written taking advantage of nose_:

.. highlight:: python

::

    from lettuce import step
    from nose.tools import assert_equals

    @step('some step with "(.*)"'):
    def some_step(step, from):
        assert_equals(from, 'expectation')

It rocks, huh?!

.. _nose: http://code.google.com/p/python-nose/
