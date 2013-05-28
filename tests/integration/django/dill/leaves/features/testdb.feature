Feature: Test running with the test database
  Scenario: Test running with the test database
    Given I have a harvester in the database:
      | make  |
      | Frank |
    Then I count the harvesters
