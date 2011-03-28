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

world.absorb
^^^^^^^^^^^^

it can be really useful to put functions and/or classes in **lettuce.world**

for example:

.. highlight:: python

.. doctest::

   from lettuce import world

   def my_project_wide_function():
       # do something

   world.my_project_wide_function = my_project_wide_function

   world.my_project_wide_function()

but as you can notice, as your project grows, there can be a lot of
repetitive lines, not DRY at all :(

in order to avoid that, lettuce provides a "absorb" decorator that lives within "world"

let's see it in action:

.. highlight:: python

.. doctest::

   from lettuce import world

   @world.absorb
   def my_project_wide_function():
       # do something

   world.my_project_wide_function()

You can also use it with classes:

.. highlight:: python

.. doctest::

   from lettuce import world

   @world.absorb
   class MyClass:
       pass

   assert isinstance(world.MyClass(), MyClass)

And even with lambdas, **but in this case you need to name it**

.. highlight:: python

.. doctest::

   from lettuce import world

   world.absorb(lambda: "yeah", "optimist_function")

   assert world.optimist_function() == 'yeah'

world.spew
^^^^^^^^^^

Well, if you read the topic above, you may be guessing: "if I keep
stashing things in lettuce.world, it may bloat it sometime, or confuse
member names along my steps, or hooks.

For those cases after **"absorbing"** something, world can also **"spew"** it.

.. highlight:: python

.. doctest::

   from lettuce import world

   @world.absorb
   def generic_function():
       # do something

   assert hasattr(world, 'generic_function')

   world.spew('generic_function')

   assert not hasattr(world, 'generic_function')

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

django-specific hooks
~~~~~~~~~~~~~~~~~~~~~

since lettuce officially suports Django_, there are a few specific hooks that help on setting up your test suite on it.

@before.harvest
^^^^^^^^^^^^^^^

this hook is ran before lettuce start harvesting your Django tests. It
can be very useful for setting up browser drivers (such as selenium),
before all tests start to run on Django.

the decorated function takes a dict with the local variables within
the `harvest` management command.

.. doctest::

   from lettuce import *
   from lettuce.django import django_url
   from selenium import selenium

   @before.harvest
   def prepare_browser_driver(variables):
       if variables.get('run_server', False) is True:
           world.browser = selenium('localhost', 4444, '*firefox', django_url('/'))
           world.browser.start()

@after.harvest
^^^^^^^^^^^^^^

this hook is ran right after lettuce finish harvesting your Django
tests. It can be very useful for shutting down previously started
browser drivers (see the example above).

the decorated function takes a list of :ref:`total-result` objects.

.. doctest::

   from lettuce import *

   @after.harvest
   def shutdown_browser_driver(results):
       world.browser.stop()

@before.each_app
^^^^^^^^^^^^^^^^

this hook is ran before lettuce run each Django_ app.

the decorated function takes the python module that corresponds to the current app.

.. doctest::

   from lettuce import *

   @before.each_app
   def populate_blog_database(app):
       if app.__name__ == 'blog':
           from blog.models import Post
           Post.objects.create(title='Nice example', body='I like writting!')

@after.each_app
^^^^^^^^^^^^^^^

this hook is ran after lettuce run each Django_ app.

the decorated function takes two arguments:

* the python module that corresponds to the current app.
* a :ref:`total-result` as parameter, so that you can use the result
statistics somehow

.. doctest::

   from lettuce import *

   @after.each_app
   def clear_blog_database_if_successful(app, result):
       if app.__name__ == 'blog':
           if result.scenarios_ran is result.scenarios_passed:
               from blog.models import Post, Comment
               Comment.objects.all()
               Post.objects.all()

@before.runserver and @after.runserver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

these hooks are ran right before, and after lettuce starts up the builtin http server.

the decorated function takes a `lettuce.django.server.ThreadedServer` object.

.. doctest::

   from lettuce import *
   from django.core.servers.basehttp import WSGIServer

   @before.runserver
   def prepare_database(server):
       assert isinstance(server, WSGIServer)
       import mydatabase
       mydatabase.prepare()

   @after.runserver
   def say_goodbye(server):
       assert isinstance(server, WSGIServer)
       print "goodbye, see you soon"

@before.handle_request and @after.handle_request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

these hooks are ran right before, and after lettuce's builtin HTTP server responds to a request.

both decorated functions takes these two arguments:

* a `django.core.servers.basehttp.WSGIServer` object.
* a `lettuce.django.server.ThreadedServer` object.

.. doctest::

   from lettuce import *
   from django.core.servers.basehttp import WSGIServer

   @before.handle_request
   def print_request(httpd, server):
       socket_object, (client_address, size) = httpd.get_request()
       print socket_object.dup().recv(size)

   @after.handle_request
   def say_goodbye(httpd, server):
       socket_object, (client_address, size) = httpd.get_request()
       print "I've just finished to respond to the client %s" % client_address

.. warning:: all the `handle_request` hooks are run within a python
   thread. If something went wrong within a calback, lettuce can get
   stuck.

.. _Django: http://djangoproject.com/
