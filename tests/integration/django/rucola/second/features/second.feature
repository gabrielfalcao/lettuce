Feature: Test the django app second
  Scenario: This one is present
    Given I say foo bar
    Then it works

  Scenario: This one is called after
    Given I say foo bar
    Then it fails