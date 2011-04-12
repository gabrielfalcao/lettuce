.. _tutorial-tables:

handling data with tables
=========================

Lets imagine writing a MVC application. While writing the tests
you will stumble in to a situation where there is a few models
that must be added to the database, maybe you will also need to check
the new state of those models.

It means that as you write tests with lettuce, it can be very useful
to handle data within steps.

Step tables are here for you

.. highlight:: ruby

::

   Feature: bill students alphabetically
     In order to bill students properly
     As a financial specialist
     I want to bill those which name starts with some letter

     Scenario: Bill students which name starts with "G"
       Given I have the following students in my database:
         | name     | monthly_due | billed |
         | Anton    | $ 500       | no     |
         | Jack     | $ 400       | no     |
         | Gabriel  | $ 300       | no     |
         | Gloria   | $ 442.65    | no     |
         | Ken      | $ 907.86    | no     |
         | Leonard  | $ 742.84    | no     |
       When I bill names starting with "G"
       Then I see those billed students:
         | Gabriel  | $ 300       | no     |
         | Gloria   | $ 442.65    | no     |
       And those that weren't:
         | Anton    | $ 500       | no     |
         | Jack     | $ 400       | no     |
         | Ken      | $ 907.86    | no     |
         | Leonard  | $ 742.84    | no     |

In the example above there are 4 steps, in which 3 contains tables.

Now let us imagine that we're using Django_ and write a step definition
that uses the table.

.. highlight:: python

::

      from lettuce import step
      from school.models import Student

      @step('I have the following students in my database:')
      def students_in_database(step):
          for student_dict in step.hashes:
              person = Student(**student_dict)
              person.save()

What about handy functions for getting the first or the last row of
the tables ?!

.. highlight:: python

::

      from lettuce import step
      from school.models import Student

      @step('I have the following students in my database:')
      def students_in_database(step):
          person1 = Student(**step.hashes.first)
          person2 = Student(**step.hashes.last)

          person1.save()
          person2.save()


Easy, huh?!

Every step has a attribute called hashes which is a list of
dicts. Each dict has represents table headers as keys and each table
row as value.

In other words, lettuce will translate the table written in the first
step as this equivalent dict

::

      @step('I have the following students in my database:')
      def students_in_database(step):
          assert step.hashes == [
              {
                  'name': 'Anton',
                  'monthly_due': '$ 500',
                  'billed': 'no'
              },
              {
                  'name': 'Jack',
                  'monthly_due': '$ 400',
                  'billed': 'no'
              },
              {
                  'name': 'Gabriel',
                  'monthly_due': '$ 300',
                  'billed': 'no'
              },
              {
                  'name': 'Gloria',
                  'monthly_due': '$ 442.65',
                  'billed': 'no'
              },
              {
                  'name': 'Ken',
                  'monthly_due': '$ 907.86',
                  'billed': 'no'
              },
              {
                  'name': 'Leonard',
                  'monthly_due': '$ 742.84',
                  'billed': 'no'
              },
          ]

.. _Django: http://djangoproject.com/
