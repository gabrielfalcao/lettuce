Feature: ignore slow steps
  As a python developer
  I want to run only the fast tests
  So that I can be really happy

  @slow-ish
  Scenario: this one is kinda slow
    Given I do nothing
    Then I see that the test passes


  @fast-ish
  Scenario: this one is fast!!
    Given I do nothing
    Then I see that the test passes
