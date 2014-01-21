Feature: Count number of emails sent
  Background:
    Given I clear my email outbox

  Scenario: Passes if mail count is expected (single)
    Given I send a test email
    Then I have sent 1 email

  Scenario: Passes if mail count is expected (multiple)
    Given I send a test email
    And I send a test email
    Then I have sent 2 emails

  # NEGATIVE TEST
  Scenario: Fails if mail count is unexpected
    Given I send a test email
    And I send a test email
    Then I have sent 1 email
