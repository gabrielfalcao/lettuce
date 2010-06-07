.. _reference-terrain:

the "terrain"
=============

terrain is a "pun" with lettuce and its "living place", its about
setup and teardown, and general hacking on your lettuce tests.

.. _terrain-py:

terrain.py
~~~~~~~~~~

by convention lettuce tries do load a file called `terrain.py` located
at the current directory.

think at this file as a global setup place, there you can setup global
hooks, and put things into lettuce "world".

.. Note::

   You can also set a `terrain.py` file within the root of your
   Django_ project, when running the `python manage.py harvest`
   command, lettuce will load it. See more at
   :ref:`the-django-command`

in practice
^^^^^^^^^^^

try out this file layout:

.. highlight:: bash

::

    /home/user/projects/some-project
           | features
                - the-name-of-my-test.feature
                - the-file-which-holds-step-definitions.py
                - terrain.py

then add some setup at `terrain.py` and run lettuce

.. highlight:: bash

::

   user@machine:~/projects/some-project$ lettuce


and notice `terrain.py` will be loaded before anything

.. _lettuce-world:
world
~~~~~

for the sake of turning easier and funnier to write tests, lettuce
"violates" some principles of good design in python, such as avoiding
implicity and using global stuff.

the "world" concept of lettuce is mostly about "global stuff".

in practice
^^^^^^^^^^^

imagine a file located somewhere that will be imported by your
application before lettuce start running tests:

.. highlight:: python

.. doctest::

   from lettuce import world

   world.some_variable = "yay!"

so that, within some step file you could use things previously set on `world`:


.. doctest::

   from lettuce import *

   @step(r'exemplify "world" by seeing that some variable contains "(.*)"')
   def exemplify_world(step, value):
       assert world.some_variable == value


and the feature could have something like:

.. highlight:: ruby

::

    Feature: test lettuce's world
      Scenario: check variable
        When I exemplify "world" by seeing that some variable contains "yay!"

hooks
~~~~~

lettuce has hooks that are called sequentially before and after each
action

presented as python decorators, it can be used to take any actions you find useful.

for example, you can set a browser driver at :ref:`lettuce-world`, and
close the connection after all, populate database with test mass or
anything you want, for example

let's see it from outside in

@before.all
^^^^^^^^^^^

this hook is ran before lettuce look for and load feature files

the decorated function takes **NO** parameters

.. highlight:: python

.. doctest::

   from lettuce import *

   @before.all
   def say_hello():
       print "Hello there!"
       print "Lettuce will start to run tests right now..."

@after.all
^^^^^^^^^^

this hook is ran after lettuce run all features, scenarios and
steps

the decorated function takes a :ref:`total-result` as parameter, so
that you can use the result statistics somehow

.. highlight:: python

.. doctest::

   from lettuce import *

   @after.all
   def say_goodbye(total):
       print "Congratulations, %d of %d scenarios passed!" % (
           total.scenarios_ran,
           total.scenarios_passed
       )
       print "Goodbye!"

@before.each_feature
^^^^^^^^^^^^^^^^^^^^

this hook is ran before lettuce run each feature

the decorated function takes a :ref:`feature-class` as parameter, so
that you can use it to fetch scenarios and steps inside.


.. highlight:: python

.. doctest::

   from lettuce import *

   @before.each_feature
   def setup_some_feature(feature):
       print "Running the feature %r, at file %s" % (
           feature.name,
           feature.described_at.file
       )

@after.each_feature
^^^^^^^^^^^^^^^^^^^

this hooks behaves in the same way @before.each_feature does, except
by the fact that its ran *after* lettuce run the feature.

.. highlight:: python

.. doctest::

   from lettuce import *

   @after.each_feature
   def teardown_some_feature(feature):
       print "The feature %r just has just ran" % feature.name

@before.each_scenario
^^^^^^^^^^^^^^^^^^^^^

this hook is ran before lettuce run each scenario

the decorated function takes a :ref:`scenario-class` as parameter, so
that you can use it to fetch steps inside.


.. highlight:: python

.. doctest::

   from lettuce import *
   from fixtures import populate_test_database

   @before.each_scenario
   def setup_some_scenario(scenario):
       populate_test_database()

@after.each_scenario
^^^^^^^^^^^^^^^^^^^^

this hooks behaves in the same way @before.each_scenario does, except
by the fact that its ran *after* lettuce run the scenario.

.. highlight:: python

.. doctest::

   from lettuce import *
   from database import models
   @after.each_scenario
   def teardown_some_scenario(scenario):
       models.reset_all_data()

@before.each_step
^^^^^^^^^^^^^^^^^

this hook is ran before lettuce run each step

the decorated function takes a :ref:`step-class` as parameter, so
that you can use it to fetch tables and so.

.. highlight:: python

.. doctest::

   from lettuce import *

   @before.each_step
   def setup_some_step(step):
       print "running step %r, defined at %s" % (
           step.sentence,
           step.defined_at.file
       )

@after.each_step
^^^^^^^^^^^^^^^^

this hooks behaves in the same way @before.each_step does, except
by the fact that its ran *after* lettuce run the step.

.. highlight:: python

.. doctest::

   from lettuce import *

   @after.each_step
   def teardown_some_step(step):
       if not step.hashes:
          print "no tables in the step"

.. _Django: http://djangoproject.com/
