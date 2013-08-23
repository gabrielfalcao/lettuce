Feature: Create models
  Scenario: Create a nice farm
    Given I have a garden in the database:
      | name          | area | raining |
      | Secret Garden | 45   | false   |
    And I have gardens in the database:
      | name             | area | raining |
      | Octopus's Garden | 120  | true    |
      | Covent Garden    | 200  | true    |
    And I have fields in the database:
      | name       |
      | Strawberry |
      | Blueberry  |
    And garden with name "Secret Garden" has fruit in the database:
      | name   | ripe_by    |
      | Apple  | 2013-07-02 |
      | Grapes | 2013-09-09 |
    And I have geese in the database:
      | name |
      | Grey |
    And I have harvesters in the database:
      | make  |
      | Frank |
      | Crank |
    And I have bees in the database:
      | name  |
      | Billy |
      | Silly |
    And fruit with name "Apple" is linked to fields in the database:
      | name       |
      | Strawberry |
    And bee with name "Billy" is linked to pollinated fruit in the database:
      | name   |
      | Apple  |
      | Grapes |
    And fruit with name "Apple" is linked to pollinated_by in the database:
      | name  |
      | Silly |
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
    "    "fields": { "raining": true, "name": "Octopus's Garden", "area": 120 }
    "  },
    "  {
    "    "pk": 3,
    "    "model": "leaves.garden",
    "    "fields": { "raining": true, "name": "Covent Garden", "area": 200 }
    "  },
    "  {
    "    "pk": 1,
    "    "model": "leaves.field",
    "    "fields": {"name": "Strawberry"}
    "  },
    "  {
    "    "pk": 2,
    "    "model": "leaves.field",
    "    "fields": {"name": "Blueberry"}
    "  },
    "  {
    "    "pk": 1,
    "    "model": "leaves.fruit",
    "    "fields": { "fields": [1], "ripe_by": "2013-07-02", "name": "Apple", "garden": 1 }
    "  },
    "  {
    "    "pk": 2,
    "    "model": "leaves.fruit",
    "    "fields": { "fields": [], "ripe_by": "2013-09-09", "name": "Grapes", "garden": 1 }
    "  },
    "  {
    "    "pk": 1,
    "    "model": "leaves.bee",
    "    "fields": {"name": "Billy", "pollinated_fruit": [1, 2]}
    "  },
    "  {
    "    "pk": 2,
    "    "model": "leaves.bee",
    "    "fields": {"name": "Silly", "pollinated_fruit": [1]}
    "  },
    "  {
    "    "pk": 1,
    "    "model": "leaves.goose",
    "    "fields": { "name": "Grey" }
    "  },
    "  {
    "    "pk": 1,
    "    "model": "leaves.harvester",
    "    "fields": { "rego": "FRA001", "make": "Frank" }
    "  },
    "  {
    "    "pk": 2,
    "    "model": "leaves.harvester",
    "    "fields": { "rego": "CRA001", "make": "Crank" }
    "  }
    "]
    """
