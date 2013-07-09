Feature: Writes to console

    As a test developer
    I want to capture my console output
    So that I can get the debugging my system wrote

    Scenario: Write to stdout
        When I write to stdout
        Then I am happy

    Scenario: write to stderr
        When I write to stderr
        Then I am happy
