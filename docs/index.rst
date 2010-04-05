.. _index:

=====================
Lettuce Documentation
=====================

Lettuce is a tool that allows python developers create plain-text,
descriptive tests in your native language.

Lettuce is a shameless clone of the super awesome Cucumber_ which does
even more than Lettuce, is more robust, and mature. But written is
mostly used for ruby.

Lettuce allows you to make BDD in the easiest way possible, without
friction to define your step definitions, a global context that lives
through with lettuce and many setup adn teardown callbacks.

Nutshell:
=========

Install ::

    user@machine:~$ [sudo] pip install lettuce

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

I was missing a tool that could be comparable to Cucumber_, but in
python.

After a pretty deep search I found a few tools for BDD in python, but none satisfied the most basic requisites:

      * Should be a nice Agile_ tool.
      * It should be so *cool* that inspire coders to make tests.
      * It could be used to test anything.

Through its development I put a few aditional goals:

      * Be compatible with cucumber, so that people that use cucumber
        to test python could migrate to lettuce with less friction.
      * It should provide ways to avoid step copy-and-paste, through a outline mechanism.
      * It should have a global context, so that different step definitions should be talk with each other.
      * It must be easy to set step definitions.

.. _Agile: http://agilemanifesto.org/
.. _Cucumber: http://cukes.info
.. _Pyccuracy: http://github.com/heynemann/pyccuracy
