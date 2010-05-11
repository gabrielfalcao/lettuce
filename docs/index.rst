 .. _index:
.. rubric:: All you need to know, from the leaves to the root

nutshell
========

**install it**

.. highlight:: bash

::

   user@machine:~$ [sudo] pip install lettuce

**describe your first feature**

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

**define its steps**

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


getting involved !
==================

**github project page**

Fork it, propose features, explore the code

`github.com/gabrielfalcao/lettuce <http://github.com/gabrielfalcao/lettuce>`_.

**feedback**

`issue tracker <http://github.com/gabrielfalcao/lettuce/issues>`_.

**discuss**

* `lettuce users mailing list <http://groups.google.com/group/lettuce-users>`_.

* `lettuce development mailing list <http://groups.google.com/group/lettuce-developers>`_.

**donate**

`support lettuce development <http://pledgie.com/campaigns/10604>`_

hands on!
=========

Is this your first experience with Lettuce ?!?

So, why not jump all and go straight to the :ref:`quick start <intro-quickstart>` ?!

introduction
============

    * **what is Lettuce, and what it does:**

      * :ref:`overview <intro-overview>`
      * :ref:`installation <intro-install>`
      * :ref:`installation <intro-install>`

what the feature ?!
-------------------

      :ref:`understand the terms behind Lettuce <intro-wtf>`

walkthrough
===========

    * **tutorial:**

      1. :ref:`writting your first feature <tutorial-simple>`
      2. :ref:`wteps with tables <tutorial-tables>`
      3. :ref:`scenario Outlines <tutorial-scenario-outlines>`
      4. :ref:`taking actions before and after tests <tutorial-hooks>`

furthermore
===========

    * **reference and concepts:**

      * :ref:`features <reference-features>`
      * :ref:`scenarios <reference-scenarios>`
      * :ref:`steps <reference-steps>`
      * :ref:`world <reference-world>`
      * :ref:`hooks <reference-hooks>`
      * :ref:`language support <reference-languages>`

recipes
=======

    * :ref:`browser testing with webdriver <recipes-webdriver>`
    * :ref:`best assertions with nose <recipes-nose>`
