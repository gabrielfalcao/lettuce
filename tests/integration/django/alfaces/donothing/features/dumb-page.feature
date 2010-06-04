Feature: Just a dumb page
  As a internet user
  I want to see a hello world page
  So that I will not find myself lonely in this world

  Scenario: Hello Lettuce at title
    Given I navigate to "/"
    Then I see the title of the page is "Hello Lettuce!"

  Scenario: A silly paragraph
    Given I navigate to "/"
    When I look inside de 1st paragraph
    Then I see it has no attributes
    And that its content is "Here comes the content!"

  Scenario: A big hello world title
    Given I navigate to "/"
    When I look inside de 1st header
    Then I see its content is "Hello World!"
    And that its id is "hello_world"
