Feature: Error traceback for output testing
  Scenario: It should pass
    Given my step that passes

  Scenario: It should raise an exception different of AssertionError
    Given my step that blows a exception
