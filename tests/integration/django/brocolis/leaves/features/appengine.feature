Feature: environment variables for GAE support
  Scenario: server name and port
    Given I start the tests
    Then I see the environment variable "SERVER_NAME" is '0.0.0.0'
    And that the environment variable "SERVER_PORT" is '8000'
