Feature: Without Header
  Background:
    Given the variable "X" holds 2

  Scenario: multiplication changing the value
    Given the variable "X" is equal to 2
    When the variable "X" holds 10
    Then the variable "X" times 5 is equal to 50
    And the variable "X" is equal to 10

  Scenario: multiplication with value set from background
    Given the variable "X" is equal to 2
    Then the variable "X" times 5 is equal to 10
    And the variable "X" is equal to 2
