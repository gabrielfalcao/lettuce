Feature: Test undefined steps are displayed on console

  Scenario: Scenario with undefined step
    Given this test step passes
    When this test step is undefined

  Scenario Outline: Outline scenario with general undefined step
    Given this test step passes
    When this test step is undefined
    Then <in> squared is <out>

  Examples:
  | in | out |
  |  1 |  1  |
  |  2 |  4  |
