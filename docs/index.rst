.. _index:

=====================
Lettuce Documentation
=====================

Lettuce is a tool that allows python developers create plain-text,
descriptive tests in your native language.

Lettuce is a shameless clone of the super awesome Cucumber_ which does
even more than Lettuce, is more robust, and mature. But written is
mostly used for ruby.

Lettuce allows you to make BDD in the easiest way possible, removing *ALL FRICTION* possible

Nutshell:
=========

Given this feature at ``~/Projects/my-projects/features/division.feature``
::
    Feature: Division
       In order to avoid silly mistakes
       Cashiers must be able to calculate a fraction
       Scenario: Regular numbers
           Given I have entered 10 into the calculator
           And I have entered 2 into the calculator
           When I press divide
           Then I see 5 as result

You can define steps at ``~/Projects/my-projects/features/step_definitions/calculator_steps.py``
    >>> from lettuce import step
    >>> from lettuce import world
    >>>
    >>> calculator_stack = []
    >>> @step(r'have entered (\d+) into the calculator')
    ... def entered_into_calculator(step, number):
    ...     calculator_stack.append(number)
    ...
    >>> @step(r'I press divide')
    ... def press_divide(step):
    ...     world.result = sum(map(int, calculator_stack))
    ...
    >>> @step(r'I see (\d+) as result')
    ... def see_result(step, result):
    ...     assert int(result) == world.result
    ...

Run with ::

    user@machine:~/Projects/my-projects/$ lettuce features/

Motivation
==========

This is not the first time I write a tool for behaviour-driven
development. I worked on Pyccuracy_ which is a awesome tool for
testing websites.

And as expected I am a hard user of Pyccuracy_, but since I met
Cucumber_, I fell in love for Scenario Outlines, global variables and
tables.  Althrough, Pyccuracy_ does not aim to do the same that
Cucumber_ does, sometimes it sucks, because Cucumber has very handy
features, that avoid code duplicity and so on.

Thus, Lettuce does not aim on website automated testing, Lettuce is a
multi-purpose testing tool.

.. _Cucumber: http://cukes.info
.. _Pyccuracy: http://github.com/heynemann/pyccuracy
