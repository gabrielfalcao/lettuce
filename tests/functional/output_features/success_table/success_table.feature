Feature: Table Success
  Scenario: Add two numbers

    Given I have 0 bucks
    And that I have these items:
      | name    | price  |
      | Porsche | 200000 |
      | Ferrari | 400000 |

    When I sell the "Ferrari"
    Then I have 400000 bucks
    And my garage contains:
      | name    | price  |
      | Porsche | 200000 |
