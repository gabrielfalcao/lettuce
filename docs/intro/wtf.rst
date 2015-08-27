.. _intro-wtf:

#####################
What the f** eature ?
#####################

Unless you are used to Cucumber_ nomenclature, you may be wondering
about the terms that surround Lettuce concepts.

If this is your case, this introduction will guide you through the
very basic keywords that cover Lettuce.

********
Features
********

Since Lettuce is used to test the behavior of a project, the behavior is broken 
up in to features of the system.

After enumerating features, you need to create scenarios which will
describe those feature. Thus, scenarios are components of a feature.

Let's learn by example: suppose we want to create a system to manage an
address book.

OK, one of the very basic features of an address book is adding contacts, which will
include their name and phone numbers.

This is how Lettuce allows you to describe such feature:

.. highlight:: ruby

::

    Feature: Add people to address book
      In order to organize phone numbers of friends
      As a wise person
      I want to add a people to my address book

      Scenario: Add a person with name and phone number
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

    In order to organize phone numbers of friends
    As a wise person
    I want to add a people to my address book

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

*********
Scenarios
*********

One or more scenarios compose a feature. There are two kinds of
scenarios:

Simple
======

The simple scenarios are composed by steps, no matter if they are
simple or tabulated steps.

The feature above is composed by two simple scenarios.

Outlined
========

Outlined scenarios are very handy because they help you to avoid
repetition.

Suppose that we need to fill the same form many times, each time
with a different data set. This is how it could be done using scenario
outlines:

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

In a nutshell, the scenario above is equivalent to write the huge code
bellow

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

As you can notice, scenario outlines are very useful and help you on
avoiding text and code repetition

*************************
Steps and its definitions
*************************

Comparable with Scenarios, Steps comes in two kinds:

Simple steps
============

Simple steps are actually simple and they are related to the step
definitions inside the scenarios.

Lettuce considers each line of a scenario as a simple step. The only
exception is if the first non-blank character of the line is a pipe
``|``. In this case, Lettuce will consider the step as a tabular step.

For instance, a simple step may look like this::

    Given I go to the conference website

Tabular steps
=============

Analog to Outlined Scenarios, the tabular steps are very useful, and
avoid repetition of text.

Tabular steps are specially useful to set up some data set in a
scenario, or to compare a set of data to the expected results in the
end of the scenario.

However, feel free to use this whenever you find it useful.

Example::

    Given I have the following contacts in my database
      | name  | phone      |
      | John  | 2233-4455  |
      | Smith | 9988-7766  |
