# language: en
Feature: Multiplication
  In order to avoid silly mistakes
  Cashiers must be able to multiplicate numbers :)

  Scenario: Regular numbers
    * I have entered 10 into the calculator
    * I have entered 4 into the calculator
    * I press multiply
    * the result should be 40 on the screen
