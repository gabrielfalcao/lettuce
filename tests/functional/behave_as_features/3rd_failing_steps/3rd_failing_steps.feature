# language: en
Feature: Multiplication
  In order to avoid silly mistakes
  Cashiers must be able to multiplicate numbers :)

  Scenario: Regular numbers
    Given I have entered 10 into the calculator
    And I have entered 4 into the calculator
    When I press multiply
    Then the result should be 40 on the screen

  Scenario: Shorter version of the scenario above
    Given I multiply 10 and 4 into the calculator
    Then the result should be 40 on the screen
