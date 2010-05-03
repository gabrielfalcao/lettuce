Feature: Failful Scenario Outline
  As lettuce author
  In order to finish the first release
  I want to make scenario outlines work :)

  Scenario Outline: fill a web form
    Given I open browser at "http://www.my-website.com/"
    And click on "sign-up"
    When I fill the field "username" with "<username>"
    And I fill the field "password" with "<password>"
    And I fill the field "password-confirm" with "<password>"
    And I fill the field "email" with "<email>"
    And I click "done"
    Then I see the message "<message>"

  Examples:
    | username | password | email          | message       |
    | john     | doe-1234 | john@gmail.org | Welcome, John |
    | mary     | wee-9876 | mary@email.com | Welcome, Mary |
    | foo      | foo-bar  | foo@bar.com    | Welcome, Foo  |
