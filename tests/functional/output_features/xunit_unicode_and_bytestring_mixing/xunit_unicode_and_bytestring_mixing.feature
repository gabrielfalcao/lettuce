Feature: Mixing of Unicode & bytestrings in xunit xml output
  Scenario Outline: It should pass
    Given non ascii characters "<value>" in outline
  Examples:
    | value    |
    | Значение |

Scenario Outline: It should pass too
    Given non ascii characters "Тест" in step

Scenario Outline: Exception should not raise an UnicodeDecodeError
    Given non ascii characters "Тест" in exception
