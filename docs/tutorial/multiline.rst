.. _tutorial-multiline:

multi-line strings
===========================

Now imagine you are writing an application which manipulates
strings. When writing the tests, you may find yourself wanting to put
multi-line strings in your steps.

Multi-line strings will do the trick

.. highlight:: ruby

::

   Feature: Split a string into multiple lines on spaces
     In order to make strings more readable
     As a user
     I want to have words split into their own lines

     Scenario: Split small-ish string
       Given I have the string "one two three four five"
       When I ask to have the string split into lines
       Then I should see the following:
         """
         one
         two
         three
         four
         five
         """

A line with nothing but three quotes (""") is used to indicate the
beginning and the end of a multi-line string.

Now, let's define a step that knows how to use this.

.. highlight:: python

::

      from lettuce import step

      @step('I should see the following:')
      def i_should_see_the_following(step):
          assert step.multiline == """one
      two
      three
      four
      five"""


Nice and straightforward.

Notice that leading spaces are stripped, and there's not a newline at
the beginning or end. This is due to the way that the parser strips
blank lines and leading and trailing whitespace.

If you need blank lines leading or trailing whitespace, you can
include lines which start and/or end with double quote, and they will
be concatenated with the other multiline lines, with the quotes
stripped off and their whitespace preserved.

For example

.. highlight:: ruby

::

   Feature: Split a string into multiple lines on spaces
     In order to make strings more readable
     As a user
     I want to have words split into their own lines

     Scenario: Split small-ish string
       Given I have the string "one two three four five"
       When I ask to have the string split into lines
       Then I should see the following:
         """
        " one
        " two  "
        "  three   "
        "   four    "
        "    five     "
        "
         """

Which we can verify like so:

.. highlight:: python

::

      from lettuce import step

      @step('I should see the following:')
      def i_should_see_the_following(step):
          assert step.multiline == '\n'.append([
          ' one',
          '  two  ',
          '   three   ',
          '    four    ',
          '     five     ',
          ''])



Admittedly, this is a hack, but there's no clean way to preserve
whitespace in only one section of a feature definition in the current
parser implementation.

Note that the first line doesn't have any whitespace at the end, and
thus doesn't need to have a quote at the end of it.

Also note that if you want a double quote at the beginning of a line
in your string, you'll have to start your line with two double quotes,
since the first one will be stripped off.