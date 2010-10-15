.. _tutorial-steps-from-step-definitions:

calling steps from step definitions
===================================

Our tests should be as expressive as possible. However, we also want to re-use steps that we've seen before. With the tools we've used so far, you could end up with seriously long step definitions.

.. highlight:: ruby

::

    Scenario: Logged-in user does something cool.
      Given I go to the home page
      And I click the login button
      And I fill in username:floppy password:banana
      And I click "Login"
      When I finally do something interesting
      Then I'm already too bored to care.
      
In this case, we probably had a test case (maybe several) for which it was actually valuable to express how the user interacted with the login form. That's where we got the step definitions for our login sequence. When the login form isn't especially interesting anymore, however, these steps are just noise. We'd really like to be able to define something like this without duplicating our step definitions.

.. highlight:: ruby

::

    Scenario: Logged-in user does something cool.
      Given I am logged in
      When I do something interesting
      Then The world becomes a better place
      
Lettuce affords you the ability to write such a "step of steps" with a set of helpers matching each of the grammar terms `Given`, `When` and `Then`. You could accomplish the above like so.

.. highlight:: python

::

    @step('I am logged in')
    def is_logged_in(step):
        step.given('I go to the home page')
        step.given('I click the login button')
        # ... and so on.
        
running blocks of steps
-----------------------

It is sometimes even desirable to run blocks of steps, copy-and-pasted directly from Feature specifications. The `Step.behave_as` method lets you do this, and you can use `string.format` to fill in parameters dynamically. For example, we can write the above step definition like so:

.. highlight:: python

::

    @step('I am logged in')
    def is_logged_in(step):
        step.behave_as("""
            Given I go to the home page
              And I click the login button
              And I fill in username:%(user)s password:%(pass)s
              And I click "Login"
        """.format({
            'user': 'floppy',
            'pass': 'banana'
        }))

This can be combined with step argument capture for step definitions that are both expressive and DRY.
