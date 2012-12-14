Feature: Unicode characters in the error traceback
  Scenario: It should pass
    Given my dæmi that passes

  Scenario: It should raise an exception different of AssertionError
    Given my "dæmi" that blows an exception
