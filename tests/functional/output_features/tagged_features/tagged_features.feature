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

  Scenario: this scenario is not tagged
    Given I do nothing
    Then I should not see "harvey@nom.cat"

  Scenario: this scenario is also not tagged
    Given some email addresses
        | email          |
        | harvey@nom.cat |
    Then I see that the test passes
