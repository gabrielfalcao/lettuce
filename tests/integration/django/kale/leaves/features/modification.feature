Feature: Live modification of view code
  Scenario: Modifications apply
    Given I change the view code
    Then the root page says "Changed"
