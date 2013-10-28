.. _index:
.. rubric:: Lettuce is a Behavior-Driven Development tool written by Gabriel Falcão G. de Moura

########
nutshell
########

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
    >>> @step
    ... def i_put_it_in_upper_case(step):
    ...     world.string = world.string.upper()
    ...
    >>> @step
    ... def see_the_string_is(step, expected):
    ...     '''I see the string is "(.*)"'''
    ...     assert world.string == expected, \
    ...         "Got %s" % world.string

**watch it pass**

.. highlight:: bash

::

   user@machine:~/Projects/my-project$ lettuce features/

##################
getting involved !
##################

**github project page**

Fork it, propose features, explore the code

`github.com/gabrielfalcao/lettuce <http://github.com/gabrielfalcao/lettuce>`_.

**feedback**

`issue tracker <http://github.com/gabrielfalcao/lettuce/issues>`_.

**discuss**

* `lettuce users mailing list <http://groups.google.com/group/lettuce-users>`_.

* `lettuce development mailing list <http://groups.google.com/group/lettuce-developers>`_.

**hack**

:doc:`/dev/index`

**donate**

`support lettuce development <http://pledgie.com/campaigns/10604>`_

#########
hands on!
#########

Is this your first experience with Lettuce ?!?

So, why don't you go straight to the :ref:`quick start tutorial <tutorial-simple>` ?!

############
introduction
############

**what is Lettuce, and what it does**

    * :ref:`overview <intro-overview>`
    * :ref:`installation <intro-install>`

what the feature ?!
*******************

    * :ref:`understand the terms behind Lettuce <intro-wtf>`

###########
walkthrough
###########

    * :ref:`write your first feature <tutorial-simple>`
    * :ref:`handling data with tables <tutorial-tables>`
    * :ref:`multi-line strings <tutorial-multiline>`
    * :ref:`don't repeat yourself, meet scenario outlines <tutorial-scenario-outlines>`
    * :ref:`clean up your spec definitions, calling one step from another <tutorial-steps-from-step-definitions>`

##########
integrate!
##########

    * :ref:`Lettuce and Django <recipes-django-lxml>`, for the sake of web development fun

###########
furthermore
###########

**reference and concepts**

    * :ref:`the command line <reference-cli>`, how to run lettuce with different verbosity levels, and other cli options
    * :ref:`features, scenarios and steps <reference-features>`, diving into lettuce's core
    * :ref:`terrain, world and hooks <reference-terrain>`, stuff about setting up a environment for lettuce
    * :ref:`language support <reference-languages>`

#######
recipes
#######

**make your own salad**

    * :ref:`nicer assertions with nose <recipes-nose>`

.. warning::
   Disclaimer on unstable features you should NOT rely on.

   For instance use the features ``step.behave_as`` and the **xunit
   XML output** are unstable and untested.

   Lettuce is a software for testing other software, but I've been
   receiving some contributions of new features that are coming
   without proper tests.

   These contributions have to be rewritten with proper tests, so that
   they won't break so often, but they are a current source of issues
   in the bug tracker.

   So until someone contributes with unit and functional tests for
   those features, or I find some time to do it myself, you should
   avoid relying on them.

   Sincerely,
   Gabriel Falcão
