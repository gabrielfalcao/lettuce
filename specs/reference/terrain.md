the "terrain"
=============

Terrain is a "pun" with lettuce and its "living place", its about setup
and teardown, and general hacking on your lettuce tests.

terrain.py
----------

By convention lettuce tries do load a file called `terrain.py` located
at the current directory.

Think at this file as a global setup place, there you can setup global
hooks, and put things into lettuce "world".

### in practice

Try out this file layout:

    /home/user/projects/some-project
           | features
                - the-name-of-my-test.feature
                - the-file-which-holds-step-definitions.py
                - terrain.py

Then add some setup at `terrain.py` and run lettuce

    user@machine:~/projects/some-project$ lettuce

And notice `terrain.py` will be loaded before anything

world
-----

For the sake of turning easier and funnier to write tests, lettuce
"violates" some principles of good design in python, such as avoiding
implicity and using global stuff.

The "world" concept of lettuce is mostly about "global stuff".

### in practice

Imagine a file located somewhere that will be imported by your
application before lettuce start running tests:

So that, within some step file you could use things previously set on
`world`:

And the feature could have something like:

    Feature: test lettuce's world
      Scenario: check variable
        When I exemplify "world" by seeing that some variable contains "yay!"

### world.absorb

It can be really useful to put functions and/or classes in
**lettuce.world**

For example:

But as you can notice, as your project grows, there can be a lot of
repetitive lines, not DRY at all :(

In order to avoid that, lettuce provides a "absorb" decorator that lives
within "world"

Let's see it in action:

You can also use it with classes:

And even with lambdas, **but in this case you need to name it**

### world.spew

Well, if you read the topic above, you may be guessing: "if I keep
stashing things in lettuce.world, it may bloat it sometime, or confuse
member names along my steps, or hooks.

For those cases after **"absorbing"** something, world can also
**"spew"** it.

hooks
-----

Lettuce has hooks that are called sequentially before and after each
action

Presented as python decorators, it can be used to take any actions you
find useful.

For example, you can set a browser driver at :ref:\`lettuce-world\`, and
close the connection after all, populate database with test mass or
anything you want, for example

Let's see it from outside in

### @before.all

This hook is ran before lettuce look for and load feature files

The decorated function takes **NO** parameters

### @after.all

This hook is ran after lettuce run all features, scenarios and steps

The decorated function takes a :ref:\`total-result\` as parameter, so
that you can use the result statistics somehow

### @before.each\_feature

This hook is ran before lettuce run each feature

The decorated function takes a :ref:\`feature-class\` as parameter, so
that you can use it to fetch scenarios and steps inside.

### @after.each\_feature

This hooks behaves in the same way @before.each\_feature does, except by
the fact that its ran *after* lettuce run the feature.

### @before.each\_scenario

This hook is ran before lettuce run each scenario

The decorated function takes a :ref:\`scenario-class\` as parameter, so
that you can use it to fetch steps inside.

### @after.each\_scenario

This hooks behaves in the same way @before.each\_scenario does, except
by the fact that its ran *after* lettuce run the scenario.

### @before.each\_step

This hook is ran before lettuce run each step

The decorated function takes a :ref:\`step-class\` as parameter, so that
you can use it to fetch tables and so.

#### @after.each\_step

This hooks behaves in the same way @before.each\_step does, except by
the fact that its ran *after* lettuce run the step.

django-specific hooks
---------------------

Since lettuce officially supports [Django](http://djangoproject.com/),
there are a few specific hooks that help on setting up your test suite
on it.

### @before.harvest

This hook is ran before lettuce start harvesting your Django tests. It
can be very useful for setting up browser drivers (such as selenium),
before all tests start to run on Django.

The decorated function takes a dict with the local variables within the
`harvest` management command.

### @after.harvest

This hook is ran right after lettuce finish harvesting your Django
tests. It can be very useful for shutting down previously started
browser drivers (see the example above).

The decorated function takes a list of :ref:\`total-result\` objects.

### @before.each\_app

This hook is ran before lettuce run each
[Django](http://djangoproject.com/) app.

The decorated function takes the python module that corresponds to the
current app.

### @after.each\_app

This hook is ran after lettuce run each
[Django](http://djangoproject.com/) app.

The decorated function takes two arguments:

-   the python module that corresponds to the current app.
-   a :ref:\`total-result\` as parameter, so that you can use the result
    statistics somehow

### @before.runserver and @after.runserver

These hooks are ran right before, and after lettuce starts up the
built-in http server.

The decorated function takes a `lettuce.django.server.ThreadedServer`
object.

### @before.handle\_request and @after.handle\_request

These hooks are ran right before, and after lettuce's built-in HTTP
server responds to a request.

Both decorated functions takes these two arguments:

-   a `django.core.servers.basehttp.WSGIServer` object.
-   a `lettuce.django.server.ThreadedServer` object.

