# language: en
Feature: Multiplication
  In order to avoid silly mistakes
  Cashiers must be able to multiplicate numbers :)

  Scenario: Regular numbers
    Given I multiply these numbers:
      | number |
      | 55     |
      | 2      |
    Then the result should be 110 on the screen

  Scenario: Shorter version of the scenario above
    Given I multiply 55 and 2 into the calculator
    Then the result should be 110 on the screen
