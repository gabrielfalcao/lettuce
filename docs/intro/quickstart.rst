.. _intro-quickstart:

About Lettuce
=============

Lettuce_ is an extremely useful and charming tool for BDD_ (Behavior
Driven Development). It can execute plain-text functional descriptions
as automated tests for Python_ projects, just as Cucumber_ does for
Ruby_.

Lettuce_ makes the development and testing process really easy,
scalable, readable and - what is best - it allows someone who doesn't
program to describe the behavior of a certain system, without
imagining those descriptions will automatically test the system during
its development.

.. image:: ./flow.png

Get Lettuce
===========

Make sure you've got Python installed and then run from the terminal:

.. highlight:: bash

::

   user@machine:~$ [sudo] pip install lettuce

Define a problem
================

Let's choose a problem to lettuce:
**Given a number, what is its factorial?**

.. Note::

   The factorial of a positive integer n, denoted by n!, is the
   product of all positive integers less than or equal to n. The
   factorial of 0 is

Project structure
=================

Build the directory tree bellow such as the files `zero.feature` and `steps.py` are empty.

.. highlight:: bash

::

    /home/user/projects/mymath
         | tests
               | features
                    - zero.feature
                    - steps.py

Lettuce it!
===========

Lets begin to describe and solve our problem...

First round
-----------


(a) Describe behaviour in English
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start describing the expected behaviour of factorial in `zero.feature` using English:

.. highlight:: ruby

::

   Feature: Compute factorial
     In order to play with Lettuce
     As beginners
     We'll implement factorial

     Scenario: Factorial of 0
       Given I have the number 0
       When I compute its factorial
       Then I see the number 1

.. Note::

    zero.feature must be inside features directory and its extension must
    be .feature. However, you're free to choose its name.

(b) Write a step definition in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, let's define the steps of the scenario, so Lettuce acan
understand the behaviour description. Write `steps.py` file using
Python:

.. highlight:: python

::

   from lettuce import *

   @step('I have the number (\d+)')
   def have_the_number(step, number):
       world.number = int(number)

   @step('I compute its factorial')
   def compute_its_fatorial(step):
       world.number = factorial(world.number)

   @step('I see the number (\d+)')
   def check_number(step, expected):
       expected = int(expected)
       assert world.number == expected, \
           "Got %d" % world.number

   def factorial(number):
       return -1

.. Note::

   `steps.py` must be inside features directory, but the names doesn't
   need to be `steps.py`, it can be any `.py` terminated file,
   Lettuce_ will look for python files recursively within features
   dir.

Ideally, factorial will be defined somewhere else. However, as this is
just a first example, we'll implement it inside steps.py, so you get
the idea of how to use Lettuce.

**Notice that, until now, we haven't defined the factorial function (it's returning -1).**

(c) Run and watch it fail
~~~~~~~~~~~~~~~~~~~~~~~~~

Go to the tests directory and run from the terminal:

.. highlight:: bash

::

   user@machine:~/projects/mymath/tests$ lettuce

As you haven't implemented factorial, it is no surprise the behavior
won't be reached:

.. image:: ./screenshot1.png

Our only scenario failed :(
Let's solve it...

(d) Write code to make the step pass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Well, by definition, we know that the factorial of 0 is 1. As our only
feature is this... we could force factorial to return 1.

.. highlight:: python

::

    from lettuce import *

    @step('I have the number (\d+)')
    def have_the_number(step, number):
        world.number = int(number)

    @step('I compute its factorial')
    def compute_its_fatorial(step):
        world.number = factorial(world.number)

    @step('I see the number (\d+)')
    def check_number(step, expected):
        expected = int(expected)
        assert world.number == expected, \
            "Got %d" % world.number

    def factorial(number):
        return 1

(e) Run again and watch it pass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Again, run from the terminal:

.. highlight:: bash

::

   user@machine:~/projects/mymath/tests$ lettuce

And you'll be happy to see your factorial implementation passed all the behaviours expected:

.. image:: ./screenshot2.png

Great! :)

However, one test is not enough for checking the quality of our
solution... So let's lettuce it again!


Second round
------------

Let's provide more tests so our problem is better described, and so we
provide a more accurate implementation of factorial:

(a) Describe behaviour in English
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's provide two new scenarios, for numbers 1 and 2:

.. highlight:: ruby

::

    Feature: Compute factorial
      In order to play with Lettuce
      As beginners
      We'll implement factorial

      Scenario: Factorial of 0
        Given I have the number 0
        When I compute its factorial
        Then I see the number 1

      Scenario: Factorial of 1
        Given I have the number 1
        When I compute its factorial
        Then I see the number 1

      Scenario: Factorial of 2
        Given I have the number 2
        When I compute its factorial
        Then I see the number 2

(b) Write a step definition in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As we haven't changed the definition, no need to make changes on this
step.

(c) Run and watch it fail
~~~~~~~~~~~~~~~~~~~~~~~~~


.. highlight:: bash

::

   user@machine:~/projects/mymath/tests$ lettuce

When running Letucce we realize that our previous implementation of
factorial works fine both for 0 and for 1, but not for 2 - it
fails. :(

.. image:: ./screenshot3.png

(d) Write code to make the step pass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's provide a solution so we get the right factorial for all
scenarions, specially for number 2:

.. highlight:: python

::

    from lettuce import *

    @step('I have the number (\d+)')
    def have_the_number(step, number):
        world.number = int(number)

    @step('I compute its factorial')
    def compute_its_fatorial(step):
        world.number = factorial(world.number)

    @step('I see the number (\d+)')
    def check_number(step, expected):
        expected = int(expected)
        assert world.number == expected, \
            "Got %d" % world.number

    def factorial(number):
        number = int(number)
        if (number == 0) or (number == 1):
            return 1
        else:
            return number

(e) Run again and watch it pass

.. highlight:: bash

::

   user@machine:~/projects/mymath/tests$ lettuce

.. image:: ./screenshot4.png

Great! Three scenarios described and they are alright!

Third round
-----------

Let's provide more tests so our problem is better described and we get
new errors so we'll be able to solve them.

(a) Describe behaviour in English
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: ruby

::

    Feature: Compute factorial
      In order to play with Lettuce
      As beginners
      We'll implement factorial

      Scenario: Factorial of 0
        Given I have the number 0
        When I compute its factorial
        Then I see the number 1

      Scenario: Factorial of 1
        Given I have the number 1
        When I compute its factorial
        Then I see the number 1

      Scenario: Factorial of 2
        Given I have the number 2
        When I compute its factorial
        Then I see the number 2

      Scenario: Factorial of 3
        Given I have the number 3
        When I compute its factorial
        Then I see the number 6

      Scenario: Factorial of 4
        Given I have the number 4
        When I compute its factorial
        Then I see the number 24

(b) Write a step definition in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As we haven't changed the definition, no need to make changes on this
step.

(c) Run and watch it fail
~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: bash

::

   user@machine:~/projects/mymath/tests$ lettuce

.. image:: ./screenshot5.png

(d) Write code to make the step pass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    from lettuce import *

    @step('I have the number (\d+)')
    def have_the_number(step, number):
        world.number = int(number)

    @step('I compute its factorial')
    def compute_its_fatorial(step):
        world.number = factorial(world.number)

    @step('I see the number (\d+)')
    def check_number(step, expected):
        expected = int(expected)
        assert world.number == expected, \
            "Got %d" % world.number

    def factorial(number):
        number = int(number)
        if (number == 0) or (number == 1):
            return 1
        else:
            return number*factorial(number-1)

(e) Run again and see the step pass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: bash

::

   user@machine:~/projects/mymath/tests$ lettuce

.. image:: ./screenshot6.png

Forth round
-----------

All steps should be repeated as long as you can keep doing them - the
quality of your software depends on these.

Have a nice lettuce...! ;)


Tips for describing similar features
====================================

On our first description file, `zero.feature`, all scenarios were
similar. This made us repeat most of the text again and again.

**Isn't there a better way to deal with this - when several scenarios are almost equal and only some values change?**

Yes, there is! :) You just need to use scenarios outlines.

An example is shown bellow:

.. highlight:: ruby

::

    Feature: Compute factorial
      In order to play with Lettuce
      As beginners
      We'll implement factorial

      Scenario Outline: Factorials [0-4]
        Given I have the number <number>
        When I compute its factorial
        Then I see the number <result>

      Examples:
        | number | result |
        | 0      | 1      |
        | 1      | 1      |
        | 2      | 2      |
        | 3      | 6      |
        | 4      | 24     |

This way, you will only need to provide the values that really change,
reducing "copy & paste" work and making your tests more clear.

.. Note::

   If you overwrite zero.feature using the example above, and goto
   step (e), you'll see your description expanding to the five
   previous scenarious:

.. image:: ./screenshot7.png

.. _Lettuce: http://lettuce.it
.. _Python: http://python.org
.. _Cucumber: http://cukes.info
.. _Ruby: http://ruby-lang.org/
.. _BDD: http://en.wikipedia.org/wiki/Behavior_Driven_Development
