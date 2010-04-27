Feature: Before and After callbacks all along lettuce
    Scenario: Before and After scenarios
        Given I append 1 in world all steps
        Then I append 2 more

    Scenario: Again
        Given I append 3 in world all steps
