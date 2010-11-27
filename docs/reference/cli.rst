.. _reference-cli:

the command line
================

Lettuce is used as a command line utility, it means that currently the
only way to use it is through a shell.

Once in a shell, you can use lettuce in 2 ways:

* in the :ref:`usual way <tutorial-simple>`

which means having the simple features/step_definitions folder
somewhere in your project

* within a :ref:`django-powered <recipes-django-lxml>` project.

the difference between them is that within Django you have more
options, but both ways have these common options:

running a specific feature file
-------------------------------

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce path/to/some/file.feature


with this option, your feature can even be out of the default ***features*** folder

running only some scenarios of a specific feature file
------------------------------------------------------

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce path/to/some/file.feature -s 3,5,9


this will run the scenarios 3, 5 and 9 from file ***path/to/some/file.feature***

running only some scenarios all feature files
---------------------------------------------

Maybe you can find it senseless, but it works like that, and does not hurt so far :)

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce -s 3,5,9

Yeah, guess what ?

This command will run the scenarios 3, 5 and 9 of all feature files living on ***myproj/features*** folder

verbosity levels
----------------


level 1 - dots for each feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce --verbosity=1

This is lettuce's minimum verbosity level. It shows dots for each step
run, regardless of what scenario or what feature is currently running

for example, if you have a feature that looks like:

.. highlight:: ruby

::

   Feature: Manipulate strings
     Scenario: Uppercased strings
       Given I have the string "lettuce leaves"
       When I put it in upper case
       Then I see the string is "LETTUCE LEAVES"


the output will be

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce -v 1
   ...

   1 feature (1 passed)
   1 scenario (1 passed)
   3 steps (3 passed)

level 2 - scenario names
~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce --verbosity=2

In this mode, lettuce will print each scenario name that is currently being ran, followed by **OK**, **FAILED** or **ERROR**
depending of the status of the steps within that scenario.

for example, if you have a feature that looks like:

.. highlight:: ruby

::

   Feature: Manipulate strings
     Scenario: Uppercased strings
       Given I have the string "lettuce leaves"
       When I put it in upper case
       Then I see the string is "LETTUCE LEAVES"

     Scenario: basic math
       Given I sum 2 and 5
       Then I see the result is 9

the output will be

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce -v 2
   Uppercased strings ... OK
   basic math ... FAILED

   1 feature (1 passed)
   2 scenarios (2 passed)
   5 steps (4 passed)

level 3 - full feature print, but colorless
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce --verbosity=3

This mode is a lot more verbose than the later one.
It prints every single feature, with really useful informations like:

* the relative path to the feature file being ran, and the current line in that file
* the relative path to the step definition responsible for the step being ran, also followed by the current line
* inline tracebacks when some feature fails
* "ready-to-use" snippets for undefined steps

for example, let's say you have the feature below, but only the step
***Given I have the string "lettuce leaves"*** is defined

.. highlight:: ruby

::

   Feature: Manipulate strings
     Scenario: Uppercased strings
       Given I have the string "lettuce leaves"
       When I put it in upper case
       Then I see the string is "LETTUCE LEAVES"

your output will look like:

.. highlight:: bash

::

    user@machine:~/projects/myproj$ lettuce -v 2

    Feature: Manipulate strings                   # features/strings.feature:1

      Scenario: Uppercased strings                # features/strings.feature:2
        Given I have the string "lettuce leaves"  # features/step_definitions/example-steps.py:5
        When I put it in upper case               # features/strings.feature:4 (undefined)
        Then I see the string is "LETTUCE LEAVES" # features/strings.feature:5 (undefined)

    1 feature (0 passed)
    1 scenario (0 passed)
    3 steps (2 undefined, 1 passed)

    You can implement step definitions for undefined steps with these snippets:

    # -*- coding: utf-8 -*-
    from lettuce import step

    @step(u'When I put it in upper case')
    def when_i_put_it_in_upper_case(step):
        assert False, 'This step must be implemented'
    @step(u'Then I see the string is "(.*)"')
    def then_i_see_the_string_is_group1(step, group1):
        assert False, 'This step must be implemented'

level 4 - full feature print, but colorful
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

this mode is almost **exactly** the same of level 3, the difference is
that it's colorful

.. image:: ../tutorial/screenshot6.png


.. note::

   If you are going to put lettuce running in a
   Continuous-Integration_ server, like Hudson_. You may choose the
   levels 1, 2 or 3, so that the output won't look messy

getting help from shell
-----------------------

.. highlight:: bash

::

   user@machine:~/projects/myproj$ lettuce -h


shows all the options described here

.. _Continuous-Integration: http://www.martinfowler.com/articles/continuousIntegration.html
.. _Hudson: http://hudson-ci.org/
