.. _reference-terrain:

the "terrain"
=============

terrain is a "pun" with lettuce and its "living place", its about
setup and teardown, and general hacking on your lettuce tests.

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

this hook is runned before lettuce look for and load feature files

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

this hook is runned after lettuce run all features, scenarios and
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

.. _Django: http://djangoproject.com/
