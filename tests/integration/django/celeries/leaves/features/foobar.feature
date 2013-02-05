Feature: Test the django app leaves
  Scenario: This one is present
    Given I say foo bar
    Then it fails

  Scenario: This one is never called
    Given I say foo bar
    Then it works
