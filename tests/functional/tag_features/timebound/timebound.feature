Feature: ignore slow steps
  As a python developer
  I want to run only the fast tests
  So that I can be really happy

  @slow-ish
  Scenario: this one is kinda slow
    Given I wait for 60 seconds
    Then the time passed is 1 minute


  @fast-ish
  Scenario: this one is fast!!
    Given I wait for 0 seconds
    Then the time passed is 0 seconds
