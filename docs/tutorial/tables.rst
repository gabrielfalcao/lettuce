.. _tutorial-tables:

Handling data with tables
=========================


Let us put that you are writting a MVC application. Along the tests
you will stumble in a kind of situation in which there is a few models
that must be added to the database. Maybe you will also need to check
the new state of those.

It means that as you write tests with lettuce, it can be very useful
to handle data within steps.

Step tables are here for you:

.. highlight:: ruby

::

   Feature: bill students alphabetically
     In order to bill students properly
     As a finantial specialist
     I want to bill those which name starts with some letter

     Scenario: Bill students which name starts with "G"
       Given I have the following students in my database:
         | name     | monthly due | billed |
         | Anton    | $ 500       | no     |
         | Jack     | $ 400       | no     |
         | John     | $ 540       | no     |
         | Garrick  | $ 438.11    | no     |
         | Gabriel  | $ 300       | no     |
         | Gloria   | $ 442.65    | no     |
         | Gaye     | $ 630.22    | no     |
         | Ken      | $ 907.86    | no     |
         | Leonard  | $ 742.84    | no     |
       When I bill names starting with "G"
       Then I see those billed students:
         | Garrick  | $ 438.11    | yes    |
         | Gabriel  | $ 300       | yes    |
         | Gloria   | $ 442.65    | yes    |
         | Gaye     | $ 630.22    | yes    |
       And those that weren't:
         | Anton    | $ 500       | no     |
         | Jack     | $ 400       | no     |
         | John     | $ 540       | no     |
         | Ken      | $ 907.86    | no     |
         | Leonard  | $ 742.84    | no     |
