Feature: Update models
  Scenario: Create a nice farm, then make it nicer
    Given I have gardens in the database:
      | id | name             | area | raining |
      | 1  | Secret Garden    | 45   | false   |
      | 2  | Octopus's Garden | 120  | true    |
      | 3  | Covent Garden    | 200  | true    |

    And I update existing gardens in the database:
      | pk | name                   | area |
      | 2  | Nicer Octopus's Garden | 150  |

    Then the database dump is as follows:
    """
    "[
    "  {
    "    "pk": 1,
    "    "model": "leaves.garden",
    "    "fields": { "raining": false, "name": "Secret Garden", "area": 45 }
    "  },
    "  {
    "    "pk": 2,
    "    "model": "leaves.garden",
    "    "fields": { "raining": true, "name": "Nicer Octopus's Garden", "area": 150 }
    "  },
    "  {
    "    "pk": 3,
    "    "model": "leaves.garden",
    "    "fields": { "raining": true, "name": "Covent Garden", "area": 200 }
    "  }
    "]
    """

  Scenario: Create a nice farm, then try to make the same farm
    Given I have gardens in the database:
      | id | name             | area | raining |
      | 1  | Secret Garden    | 45   | false   |
      | 2  | Octopus's Garden | 120  | true    |
      | 3  | Covent Garden    | 200  | true    |

    And I have gardens in the database:
      | pk | name                   | area |
      | 2  | Nicer Octopus's Garden | 150  |
