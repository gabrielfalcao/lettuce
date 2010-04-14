 .. _index:
.. rubric:: All you need to know, from the leaves to the root

Quickstart
==========

**install it**

.. highlight:: bash

::

   user@machine:~$ [sudo] pip install lettuce

**Describe your first feature**

.. highlight:: ruby

::

   Feature: Manipulate strings
     In order to have some fun
     As a programming beginner
     I want to manipulate strings

     Scenario: Uppercased strings
       Given I have the string "lettuce leaves"
       When I put it in upper case
       Then I see the string is "LETTUCE LEAVES"

**Define its steps**

.. highlight:: python

.. doctest::

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

.. highlight:: bash
::

   user@machine:~/Projects/my-project$ lettuce features/

Introduction
============

    * **What is Lettuce, and what it does:**

      * :ref:`Overview <intro-overview>`
      * :ref:`Installation <intro-install>`

What the feature ?!
-------------------

      :ref:`Understand the terms behind Lettuce <intro-wtf>`

Walkthrough
===========

    * **Tutorial:**

      1. :ref:`Writting your first feature <tutorial-simple>`
      2. :ref:`Steps with tables <tutorial-tables>`
      3. :ref:`Scenario Outlines <tutorial-scenario-outlines>`
      4. :ref:`Taking actions before and after tests <tutorial-hooks>`

Furthermore
===========

    * **Reference and concepts:**

      * :ref:`Features <reference-features>`
      * :ref:`Scenarios <reference-scenarios>`
      * :ref:`Steps <reference-steps>`
      * :ref:`World <reference-world>`
      * :ref:`Hooks <reference-hooks>`
      * :ref:`Language support <reference-languages>`

Recipes
=======

    * :ref:`Browser testing with webdriver <recipes-webdriver>`
    * :ref:`Best assertions with nose <recipes-nose>`
