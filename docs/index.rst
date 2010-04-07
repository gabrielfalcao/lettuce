 .. _index:
.. rubric:: All you need to know, from the leaves to the root

Quickstart
==========

**install it**

::

   user@machine:~$ [sudo] pip install lettuce

**Describe your first feature**

::

   Feature: Manipulate string
     In order to have some fun
     As a programming beginner
     I want to manipulate strings

     Scenario: Uppercased strings
       Given I have the string "lettuce leaves"
       When I put it in upper case
       Then I see the string is "LETTUCE LEAVES"

**Define its steps**

::

    >>> from lettuce import *
    >>> @step('I have the string "(.*)"')
    ... def have_the_string(step, string):
    ...     world.string = string
    ...
    >>> @step('I put it in upper case')
    ... def put_it_in_upper(step):
    ...     world.string = world.string.upper()
    ...
    >>> @step('I see the string is "(.*)"')
    ... def see_the_string_is(step, expected):
    ...     assert world.string == expected, \
    ...         "Got %s" % world.string

**watch it pass**

::

   user@machine:~/Projects/my-project$ lettuce features/

First steps
===========

    * **What is Lettuce, and what it does:**

      * :ref:`Overview <intro-overview>`
      * :ref:`Installation <intro-install>`

    * **Tutorial:**

      * :ref:`Simple features <tutorial-simple>`
      * :ref:`Steps with tables <tutorial-tables>`
      * :ref:`Scenario Outlines <tutorial-scenario-outlines>`
      * :ref:`Taking actions before and after tests <tutorial-hooks>`

    * **Reference and concepts:**

      * :ref:`Features <reference-features>`
      * :ref:`Scenarios <reference-scenarios>`
      * :ref:`Steps <reference-steps>`
      * :ref:`Hooks <reference-hooks>`
      * :ref:`World <reference-world>`
      * :ref:`Language support <reference-languages>`

Recipes
=======

    * :ref:`Browser testing with webdriver <recipes-webdriver>`
    * :ref:`Best assertions with nose <recipes-nose>`
