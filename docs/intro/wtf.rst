.. _intro-wtf:

=====================
What the f** eature ?
=====================

Unless you are used to Cucumber_ nomenclature, you may be wondering
about the terms that surround Lettuce concepts.

If this is your case, this introduction will guide you through the
very basic keywords that concept Lettuce.


Features
========

Since Lettuce is based on the *behaviour* of the project that is being
designed, you will think on features.

After enumerating features, you will create scenarios to describe its
feature. Thus, scenarios are components of a feature.

Let's learn by example, supposing we want to create a system to manage
a contact book.

OK, one of the very basic feature of a contact book is adding names
and phones of a person.

See how this feature could be described with Lettuce above:


.. highlight:: ruby

::

    Feature: Add people to contact book
      In order to organize phones of friends
      As a wise person
      I want to add a people to my contact book

      Scenario: Add a person with name and phone
        Given I fill the field "name" with "John"
        And fill the field "phone" with "2233-4455"
        When I save the data
        Then I see that my contact book has the persons:
          | name | phone     |
          | John | 2233-4455 |

      Scenario: Avoiding a invalid phone number
        Given I fill the field "name" with "John"
        And fill the field "phone" with "000"
        When I save the data
        Then I get the error: "000 is a invalid phone number"

In the feature above we can notice a few elements, for instance:

 * The feature name:

 ::

  Feature: Add people to contact book

 * Feature headline:

 ::

     In order to organize phones of friends
     As a wise person
     I want to add a people to my contact book

 * Scenarios:

 ::

     Scenario: Add a person with name and phone
       Given I fill the field "name" with "John"
       And fill the field "phone" with "2233-4455"
       When I save the data
       Then I see that my contact book has the persons:
         | name | phone     |
         | John | 2233-4455 |

     Scenario: Avoiding a invalid phone number
       Given I fill the field "name" with "John"
       And fill the field "phone" with "000"
       When I save the data
       Then I get the error: "000 is a invalid phone number"

Scenarios
=========

One or more scenarios compose a feature. And there are two kinds of scenarios:

Simple
~~~~~~

The simple scenarios are composed by steps, no matter if they are
simple or tabulated steps.

The feature above is composed by two simple scenarios.

Outlined
~~~~~~~~

Outlined scenarios are very handy and avoid repetition.

Supposing that we need fill the same formulary many times, each time
with a different data set.

Let's see how it could be done with scenario outlines:

::

    Feature: Apply all my friends to attend a conference
      In order to apply all my friends to the next PyCon_
      As a lazy person
      I want to fill the same form many times

      Scenario Outline: Apply my friends
        Go to the conference website
        Access the link "I will attend"
        Fill the field "name" with "<friend_name>"
        Fill the field "email" with "<friend_email>"
        Fill the field "birthday" with "<friend_birthdate>"
        Click on "confirm attendance" button

      Examples:
        | friend_name | friend_email         | friend_birthdate |
        | Mary        | mary@domain.com      | 1988/02/10       |
        | Lincoln     | lincoln@provider.net | 1987/09/10       |
        | Marcus      | marcus@other.org     | 1990/10/05       |

In a nutshell, the scenario above is equivalent to write this amount of text:

::

    Feature: Apply all my friends to attend a conference
      In order to apply all my friends to the next PyCon_
      As a lazy person
      I want to fill the same form many times

      Scenario: Apply Mary
        Go to the conference website
        Access the link "I will attend"
        Fill the field "name" with "Mary"
        Fill the field "email" with "mary@domain.com"
        Fill the field "birthday" with "1988/02/10"
        Click on "confirm attendance" button

      Scenario: Apply Lincoln
        Go to the conference website
        Access the link "I will attend"
        Fill the field "name" with "Lincoln"
        Fill the field "email" with "lincoln@provider.net"
        Fill the field "birthday" with "1987/09/10"
        Click on "confirm attendance" button

      Scenario: Apply Marcus
        Go to the conference website
        Access the link "I will attend"
        Fill the field "name" with "Marcus"
        Fill the field "email" with "marcus@other.org"
        Fill the field "birthday" with "1990/10/05"
        Click on "confirm attendance" button

As you can notice, scenario outlines are really useful and help you to
avoid repetition of text and code.

Steps and its definitions
=========================

Comparable with Scenarios, Steps comes in two kinds:

Simple steps
~~~~~~~~~~~~

Simple steps are actually simple, they are matched with step
definitions.

Lettuce considers each line of a scenario as a simple step, the only
exception is if the first non-blank character of the line is a pipe
``|``, in this case Lettuce will consider the step as a tabular step.

In a nutshell, a simple step may look like this::

    Given I go to the conference website

Tabular steps
~~~~~~~~~~~~~

Analog to Outlined Scenarios, the tabular steps are very useful, and
avoid repetition of text.

Tabular steps are specially useful to set up some data set in aa
scenario, or compare a set of data to results at the end of the
scenario.

But nothing avoid you to use at your will.

Example::

    Given I have the following contacts in my database
      | name  | phone      |
      | John  | 2233-4455  |
      | Smith | 9988-7766  |

.. _Agile: http://agilemanifesto.org
.. _Cucumber: http://cukes.info
.. _Pyccuracy: http://github.com/heynemann/pyccuracy
.. _TDD: http://en.wikipedia.org/wiki/Test_Driven_Development
.. _BDD: http://en.wikipedia.org/wiki/Behavior_Driven_Development
