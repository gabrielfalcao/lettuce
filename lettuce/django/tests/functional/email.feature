Feature: Check email sent by Django server

Scenario: Access a web page which triggers an email
    Given I visit "/mail/"
    Then I see "Mail has been sent"
    and an email is sent to "to@example.com" with subject "Subject here"

