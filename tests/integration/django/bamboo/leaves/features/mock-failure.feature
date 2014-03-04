Feature: Mock an email error
  Background:
    Given I clear my email outbox

  Scenario: Fail...
    Given sending email does not work

    When I send a test email with the following set:
      """
      " from_email: 'orders@bamboodirect.com'
      " to:
      "   - 'shipping@bamboodirect.com'
      " subject: New Order
      " body: |
      "         Order ID: 10
      "         Name: Mr Panda
      "         Quantity: Many
      """
