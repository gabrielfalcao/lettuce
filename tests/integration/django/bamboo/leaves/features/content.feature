Feature: Count number of emails sent
  Background:
    Given I clear my email outbox

  Scenario: Body content check, single email
    Given I send a test email with the following set:
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

    Then I have sent an email with the following in the body:
      """
      Name: Mr Panda
      Quantity: Many
      """

  Scenario: Body content check, multiple emails
    Given I send a test email with the following set:
      """
      " from_email: orders@bamboodirect.com
      " to:
      "   - shipping@bamboodirect.com
      " subject: New Order
      " body: |
      "         Order ID: 10
      "         Name: Fluffy Bear
      "         Quantity: Quite a few
      """
    And I send a test email with the following set:
      """
      " from_email: orders@bamboodirect.com
      " to:
      "   - shipping@bamboodirect.com
      " subject: New Order
      " body: |
      "         Name: Mr Panda
      "         Quantity: Many
      "         Notes: This guy really likes bamboo
      """
    And I send a test email with the following set:
      """
      " from_email: orders@bamboodirect.com
      " to:
      "   - shipping@bamboodirect.com
      " subject: New Order
      " body: |
      "         Order ID: 12
      "         Name: Guy Rollsaround
      "         Quantity: A bunch
      """

    Then I have sent an email with the following in the body:
      """
      Name: Mr Panda
      Quantity: Many
      """

  # NEGATIVE TEST
  Scenario: Fail if content is not found
    Given I send a test email with the following set:
      """
      " from_email: orders@bamboodirect.com
      " to:
      "   - shipping@bamboodirect.com
      " subject: New Order
      " body: |
      "         Order ID: 10
      "         Name: Fluffy Bear
      "         Quantity: Quite a few
      """

    Then I have sent an email with the following in the body:
      """
      Name: Badger
      Quantity: None
      """