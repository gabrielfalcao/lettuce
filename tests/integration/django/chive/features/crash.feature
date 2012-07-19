Feature: server crashed
  Scenario: Crashing from hooks
    Given I go to "/"
    Then I get a 404
