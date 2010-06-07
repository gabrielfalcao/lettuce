.. _recipes-django-lxml:

Web development fun with Lettuce and Django
===========================================

Django_ is a awesome web framework, very mature, aims on simplicity
and the best of all: it's funny to use it.

To make it even funny, lettuce has builtin support to Django.

Getting started
~~~~~~~~~~~~~~~

1. install the lettuce django app
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pick up any django project, and add ``lettuce.django`` in its
``settings.py`` configuration file:

::

   INSTALLED_APPS = (
       'django.contrib.auth',
       'django.contrib.admin',

       # ... other apps here ...
       'my_app',
       'lettuce.django', # this guy will do the job :)
   )

considering the configuration above, let's say we want to write tests
to ``my_app`` django application.

2. create the feature directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

lettuce will look for a ``features`` folder inside every installed app:

::

    /home/user/projects/djangoproject
         | settings.py
         | manage.py
         | urls.py
         | my_app
               | features
                    - index.feature
                    - index-steps.py

3. write your first feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``@index.feature``:

.. highlight:: ruby

::

    Feature: Rocking with lettuce and django

        Scenario: Simple Hello World
            Given I access the url "/"
            Then I see the header "Hello World"

        Scenario: Hello + capitalized name
            Given I access the url "/some-name"
            Then I see the header "Hello Some Name"


``@index-steps.py``:

.. highlight:: python

::

    from lettuce import *
    from lxml import html
    from django.test.client import Client
    from nose.tools import assert_equals

    @before.all
    def set_browser():
        world.browser = Client()

    @step(r'I access the url "(.*)"')
    def access_url(step, url):
        response = world.browser.get(url)
        world.dom = html.fromstring(response.content)

    @step(r'I see the header "(.*)"')
    def see_header(step, text):
        header = world.dom.cssselect('h1')[0]
        assert header.text == text

4. run th tests
^^^^^^^^^^^^^^^

once you install the ``lettuce.django`` app, the command ``harvest`` will be available:

.. highlight:: bash

::

   user@machine:~projects/djangoproject $ python manage.py harvest


5. that is all folks!
^^^^^^^^^^^^^^^^^^^^^

write views to make tests pass, write more feature files, and rock out
loud with lettuce :)


actual example code
~~~~~~~~~~~~~~~~~~~

In order to assure that lettuce integrate well with django, it have a
set of integration tests, there are a actual django project running
with lettuce.

You can grab the code at the alfaces_ folder of lettuce git repository

Technical details
=================

If you want to write acceptance tests that run with web browsers, you
can user tools like twill_, selenium_, webdriver_ and windmill_

red-tape-less builtin server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lettuce cleverly runs the a instance of django builtin http server in
background, it tries to bind the HTTP server at localhost:8000 but if
the port is busy, it keeps trying to run in higher ports: 8001, 8002
and so on until it reaches the max port number 65535

So that you can use browser-based tools such as those listed above to
access Django.

figure out django urls
~~~~~~~~~~~~~~~~~~~~~~

As django http server can be running in any port within the range
8000 - 65535, it could be hard to figure out the correct URL for your
project, right ?

Wrong!

Lettuce is here for you. Within your steps you can use the
``django_url`` utility function:

.. highlight:: python

::

    from lettuce import step, world
    from lettuce.django import django_url

    @step(r'Given I navigate to "(.*)"')
    def navigate_to_url(step, url):
        full_url = django_url(url)
        world.browser.get(full_url)


what does ``django_url`` do ?!?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It prepends a django-internal url with the HTTP server address.

In other words, if lettuce binds the http server to localhost:9090 and
you call ``django_url`` with ``"/admin/login"``:

.. highlight:: python

::

    from lettuce.django import django_url
    django_url("/admin/login")

it returns:

.. highlight:: python

::

    "http://localhost:9090/admin/login"

terrain also available in django projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

at this point you probably know how :ref:`terrain-py` works, and it
also works with django projects.

you can setup environment and stuff like that within a ``terrain.py``
file located at the root of your django project.

taking the very first example of this documentation page, your django
project layout would like like this:

::

    /home/user/projects/djangoproject
         | settings.py
         | manage.py
         | urls.py
         | terrain.py
         | my_app
               | features
                    - index.feature
                    - index-steps.py

notice the ``terrain.py`` file at the project root, there you can
populate the :ref:`lettuce-world` and organize your features and steps
with it :)

.. _alfaces: http://github.com/gabrielfalcao/lettuce/tree/master/tests/integration/django/alfaces/
.. _Django: http://djangoproject.com
.. _twill: http://twill.idyll.org/python-api.html
.. _selenium: http://seleniumhq.org/docs/appendix_installing_python_driver_client.html
.. _windmill: http://www.getwindmill.com/
.. _webdriver: http://code.google.com/p/selenium/wiki/PythonBindings?redir=1
