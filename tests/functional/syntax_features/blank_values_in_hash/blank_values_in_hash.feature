Feature: Allow blanks in steps

  Scenario: blank values default to blank strings
    Given I ignore step
    When I ignore step
    Then the string length calc should be correct:
     | string | string2 | length | 
     | car    | bike    | 7      |
     |        | bike    | 4      |
     | car    |         | 3      |
    And I ignore step
