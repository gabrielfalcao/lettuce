Feature: avoid duplicating same snippet
  Scenario: Propose matched groups
    Given I have "stuff here" and "more @#$%ˆ& bizar sutff h3r3"
    Given I have "blablabla" and "12345"
