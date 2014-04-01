Feature: Django HTTP Threading support
  Scenario: Check threading http server
    Given I navigate to "/" with 4 threads
    Then I see 5 threads in server execution
    Then I wait all requests
    Then all requests was finishing in pararell mode
