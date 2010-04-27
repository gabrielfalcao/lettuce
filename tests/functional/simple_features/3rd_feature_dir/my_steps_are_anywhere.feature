Feature: Having step definition all along folders
  In order to find step definition files
  As a nice lib
  I will look for step definitions recursively
  Scenario: Looking for steps anywhere
    Given I define step at look/here/step_one.py
    And at look/and_here/step_two.py
    Also at look/here/for_steps/step_three.py
    And finally at look/and_here/and_any_python_file/step_four.py
