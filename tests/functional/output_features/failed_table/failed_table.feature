Feature: Table Fail
  Scenario: See it fail

    Given I have a dumb step that passes

    And this one fails

    Then this one will be skipped

    And this one will be skipped

    And this one does not even has definition
