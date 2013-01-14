# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from sure import that, expect
from lettuce import step
from lettuce.core import Scenario
from lettuce.core import Feature
from lettuce.core import Background
from lettuce.core import HashList
from lettuce.exceptions import LettuceSyntaxError
from nose.tools import assert_equals

FEATURE1 = """
Feature: Rent movies
    Scenario: Renting a featured movie
        Given I have the following movies in my database
           | Name                    | Rating  | New | Available |
           | Matrix Revolutions      | 4 stars | no  | 6         |
           | Iron Man 2              | 5 stars | yes | 11        |
        When the client 'John Doe' rents 'Iron man 2'
        Then he needs to pay 10 bucks

    Scenario: Renting a non-featured movie
        Given I have the following movies in my database
           | Name                    | Rating  | New | Available |
           | A night at the museum 2 | 3 stars | yes | 9         |
           | Matrix Revolutions      | 4 stars | no  | 6         |
        When the client 'Mary Doe' rents 'Matrix Revolutions'
        Then she needs to pay 6 bucks

    Scenario: Renting two movies allows client to take one more without charge
        Given I have the following movies in my database
           | Name                    | Rating  | New | Available |
           | A night at the museum 2 | 3 stars | yes | 9         |
           | Matrix Revolutions      | 4 stars | no  | 6         |
           | Iron Man 2              | 5 stars | yes | 11        |
        When the client 'Jack' rents 'Iron man 2'
        And also rents 'Iron man 2' and 'A night at the museum 2'
        Then he needs to pay 16 bucks
"""

FEATURE2 = """
Feature: Division
      In order to avoid silly mistakes
      Cashiers must be able to calculate a fraction

      Scenario: Regular numbers
            * I have entered 3 into the calculator
            * I have entered 2 into the calculator
            * I press divide
            * the result should be 1.5 on the screen
"""

FEATURE3 = """
Feature: A long line as feature name will define the max length of the feature
  In order to describe my features
  I want to add description on them
  Scenario: Regular numbers
    Nothing to do
"""

FEATURE4 = """
Feature: Big sentence
  As a clever guy
  I want to describe this Feature
  So that I can take care of my Scenario
  Scenario: Regular numbers
    Given a huge sentence, that have so many characters
    And another one, very tiny
"""

FEATURE5 = """
Feature: Big table
  Scenario: Regular numbers
    Given that I have these items:
      | description                                                               |
      | this is such a huge description within a table, the maxlengh will be huge |
      | this is another description within a table                                |
"""

FEATURE6 = """
Feature: Big scenario outline
  Scenario: Regular numbers
    Given I do fill 'description' with '<value_two>'
  Examples:
    | value_two                                                               |
    | this is such a huge value within a table, the maxlengh will be damn big |
    | this is another description within a table                              |

"""

FEATURE7 = """
Feature: Big table
  Scenario: Regular numbers
    Given that I have these items:
      | description-long-as-hell | name-that-will-make-my-max-length-big |
      | one                      | john                                  |
      | two                      | baby                                  |
"""

FEATURE8 = """
Feature: Big scenario outline
  Scenario: big scenario outlines
    Given I do fill 'description' with '<value_two>'

  Examples:
    | value_two_thousand_and_three | another_one | and_even_bigger |
    | 1                            | um          | one             |
    | 2                            | dois        | two             |
"""

FEATURE9 = """
Feature: Big scenario outline
  Scenario: big scenario outlines
    Given I do fill 'description' with '<value_two>'

  Examples:
    | value_two_thousand_and_three_biiiiiiiiiiiiiiiiiiiiiiiiiiiiig |
    | 1                                                            |
    | 2                                                            |
    | 3                                                            |
"""

FEATURE10 = """
Feature: Big sentence
  As a clever guy
  I want to describe this Feature
  So that I can take care of my Scenario
  Scenario: Regular numbers
    Given a huge sentence, that have so many characters
    And another one, very tiny

    # Feature: Big sentence
    #   As a clever guy
    #   I want to describe this Feature
    #   So that I can take care of my Scenario
    #   Scenario: Regular numbers
    #     Given a huge sentence, that have so many characters
    #     And another one, very tiny
"""

FEATURE11 = """
Feature: Yay tags
  @many @other
  @basic
  @tags @here @:)
  Scenario: Double Yay
    Given this scenario has tags
    Then it can be inspected from within the object
"""

FEATURE12 = """
Feature: Yay tags and many scenarios
  @many @other
  @basic
  @tags @here @:)
  Scenario: Holy tag, Batman
    Given this scenario has tags
    Then it can be inspected from within the object

  @only
  @a-few @tags
  Scenario: Holy guacamole
    Given this scenario has tags
    Then it can be inspected from within the object

"""

FEATURE13 = '''
Feature: correct matching
  @runme
  Scenario: Holy tag, Batman
    Given this scenario has tags
    Then it can be inspected from within the object

  Scenario: This has no tags
    Given this scenario has no tags
    Then I fill my email with gabriel@lettuce.it

  @slow
  Scenario: this is slow
    Given this scenario has tags
    When I fill my email with "gabriel@lettuce.it"
    Then it can be inspected from within the object

  Scenario: Also without tags
    Given this scenario has no tags
    Then I fill my email with 'gabriel@lettuce.it'
'''

FEATURE14 = """
Feature:    Extra whitespace feature
  I want to match scenarios with extra whitespace
  Scenario:    Extra whitespace scenario
    Given this scenario, which has extra leading whitespace
    Then the scenario definition should still match
"""

FEATURE15 = """
Feature: Redis database server

    Scenario: Bootstraping Redis role
        Given I have a an empty running farm
        When I add redis role to this farm
        Then I expect server bootstrapping as M1
        And scalarizr version is last in M1
        And redis is running on M1

    Scenario: Restart scalarizr
        When I reboot scalarizr in M1
        And see 'Scalarizr terminated' in M1 log
        Then scalarizr process is 2 in M1
        And not ERROR in M1 scalarizr log

    @rebundle
    Scenario: Rebundle server
        When I create server snapshot for M1
        Then Bundle task created for M1
        And Bundle task becomes completed for M1

    @rebundle
    Scenario: Use new role
        Given I have a an empty running farm
        When I add to farm role created by last bundle task
        Then I expect server bootstrapping as M1

    @rebundle
    Scenario: Restart scalarizr after bundling
        When I reboot scalarizr in M1
        And see 'Scalarizr terminated' in M1 log
        Then scalarizr process is 2 in M1
        And not ERROR in M1 scalarizr log

    Scenario: Bundling data
        When I trigger databundle creation
        Then Scalr sends DbMsr_CreateDataBundle to M1
        And Scalr receives DbMsr_CreateDataBundleResult from M1
        And Last databundle date updated to current

    Scenario: Modifying data
        Given I have small-sized database 1 on M1
        When I create a databundle
        And I terminate server M1
        Then I expect server bootstrapping as M1
        And M1 contains database 1

    Scenario: Reboot server
        When I reboot server M1
        Then Scalr receives RebootStart from M1
        And Scalr receives RebootFinish from M1

    Scenario: Backuping data on Master
        When I trigger backup creation
        Then Scalr sends DbMsr_CreateBackup to M1
        And Scalr receives DbMsr_CreateBackupResult from M1
        And Last backup date updated to current

    Scenario: Setup replication
        When I increase minimum servers to 2 for redis role
        Then I expect server bootstrapping as M2
        And scalarizr version is last in M2
        And M2 is slave of M1

    Scenario: Restart scalarizr in slave
        When I reboot scalarizr in M2
        And see 'Scalarizr terminated' in M2 log
        Then scalarizr process is 2 in M2
        And not ERROR in M2 scalarizr log

    Scenario: Slave force termination
        When I force terminate M2
        Then Scalr sends HostDown to M1
        And not ERROR in M1 scalarizr log
        And redis is running on M1
        And scalarizr process is 2 in M1
        Then I expect server bootstrapping as M2
        And not ERROR in M1 scalarizr log
        And not ERROR in M2 scalarizr log
        And redis is running on M1

    @ec2
    Scenario: Slave delete EBS
        When I know M2 ebs storage
        And M2 ebs status is in-use
        Then I terminate server M2 with decrease
        And M2 ebs status is deleting
        And not ERROR in M1 scalarizr log

    @ec2
    Scenario: Setup replication for EBS test
        When I increase minimum servers to 2 for redis role
        Then I expect server bootstrapping as M2
        And M2 is slave of M1

    Scenario: Writing on Master, reading on Slave
        When I create database 2 on M1
        Then M2 contains database 2

    Scenario: Slave -> Master promotion
        Given I increase minimum servers to 3 for redis role
        And I expect server bootstrapping as M3
        When I create database 3 on M1
        And I terminate server M1 with decrease
        Then Scalr sends DbMsr_PromoteToMaster to N1
        And Scalr receives DbMsr_PromoteToMasterResult from N1
        And Scalr sends DbMsr_NewMasterUp to all
        And M2 contains database 3

    @restart_farm
    Scenario: Restart farm
        When I stop farm
        And wait all servers are terminated
        Then I start farm
        And I expect server bootstrapping as M1
        And scalarizr version is last in M1
        And redis is running on M1
        And M1 contains database 3
        Then I expect server bootstrapping as M2
        And M2 is slave of M1
        And M2 contains database 3
"""

FEATURE16 = """
Feature: Movie rental
    As a rental store owner
    I want to keep track of my clients
    So that I can manage my business better

    Background:
        Given I have the following movies in my database:
           | Name                    | Rating  | New | Available |
           | Matrix Revolutions      | 4 stars | no  | 6         |
           | Iron Man 2              | 5 stars | yes | 11        |
        And the following clients:
           | Name      |
           | John Doe  |
           | Foo Bar   |

    Scenario: Renting a featured movie
        Given the client 'John Doe' rents 'Iron Man 2'
        Then there are 10 more left

    Scenario: Renting an old movie
        Given the client 'Foo Bar' rents 'Matrix Revolutions'
        Then there are 5 more left
"""

FEATURE17 = """
Feature: Movie rental without MMF
    Background:
        Given I have the following movies in my database:
           | Name                    | Rating  | New | Available |
           | Matrix Revolutions      | 4 stars | no  | 6         |
           | Iron Man 2              | 5 stars | yes | 11        |
        And the following clients:
           | Name      |
           | John Doe  |
           | Foo Bar   |

    Scenario: Renting a featured movie
        Given the client 'John Doe' rents 'Iron Man 2'
        Then there are 10 more left
"""

FEATURE18 = """
Feature: My scenarios have no name
    Scenario:
        Given this scenario raises a syntax error
"""


def test_feature_has_repr():
    "Feature implements __repr__ nicely"
    feature = Feature.from_string(FEATURE1)
    expect(repr(feature)).to.equal('<Feature: "Rent movies">')


def test_scenario_has_name():
    "It should extract the name string from the scenario"

    feature = Feature.from_string(FEATURE1)

    assert isinstance(feature, Feature)

    expect(feature.name).to.equal("Rent movies")


def test_feature_has_scenarios():
    "A feature object should have a list of scenarios"

    feature = Feature.from_string(FEATURE1)

    expect(feature.scenarios).to.be.a(list)
    expect(feature.scenarios).to.have.length_of(3)

    expected_scenario_names = [
        "Renting a featured movie",
        "Renting a non-featured movie",
        "Renting two movies allows client to take one more without charge",
    ]

    for scenario, expected_name in zip(feature.scenarios, expected_scenario_names):
        expect(scenario).to.be.a(Scenario)
        expect(scenario.name).to.equal(expected_name)

    expect(feature.scenarios[1].steps[0].keys).to.equal(
        ('Name', 'Rating', 'New', 'Available'))

    expect(list(feature.scenarios[1].steps[0].hashes)).to.equal([
        {
            'Name': 'A night at the museum 2',
            'Rating': '3 stars',
            'New': 'yes',
            'Available': '9',
        },
        {
            'Name': 'Matrix Revolutions',
            'Rating': '4 stars',
            'New': 'no',
            'Available': '6',
        },
    ])


def test_can_parse_feature_description():
    "A feature object should have a description"

    feature = Feature.from_string(FEATURE2)

    assert_equals(
        feature.description,
        "In order to avoid silly mistakes\n"
        "Cashiers must be able to calculate a fraction"
    )
    expected_scenario_names = ["Regular numbers"]
    got_scenario_names = [s.name for s in feature.scenarios]

    assert_equals(expected_scenario_names, got_scenario_names)
    assert_equals(len(feature.scenarios[0].steps), 4)

    step1, step2, step3, step4 = feature.scenarios[0].steps

    assert_equals(step1.sentence, '* I have entered 3 into the calculator')
    assert_equals(step2.sentence, '* I have entered 2 into the calculator')
    assert_equals(step3.sentence, '* I press divide')
    assert_equals(step4.sentence, '* the result should be 1.5 on the screen')

def test_scenarios_parsed_by_feature_has_feature():
    "Scenarios parsed by features has feature"

    feature = Feature.from_string(FEATURE2)

    for scenario in feature.scenarios:
        assert_equals(scenario.feature, feature)

def test_feature_max_length_on_scenario():
    "The max length of a feature considering when the scenario is longer than " \
    "the remaining things"

    feature = Feature.from_string(FEATURE1)
    assert_equals(feature.max_length, 76)

def test_feature_max_length_on_feature_description():
    "The max length of a feature considering when one of the description lines " \
    "of the feature is longer than the remaining things"

    feature = Feature.from_string(FEATURE2)
    assert_equals(feature.max_length, 47)

def test_feature_max_length_on_feature_name():
    "The max length of a feature considering when the name of the feature " \
    "is longer than the remaining things"

    feature = Feature.from_string(FEATURE3)
    assert_equals(feature.max_length, 78)

def test_feature_max_length_on_step_sentence():
    "The max length of a feature considering when the some of the step sentences " \
    "is longer than the remaining things"

    feature = Feature.from_string(FEATURE4)
    assert_equals(feature.max_length, 55)

def test_feature_max_length_on_step_with_table():
    "The max length of a feature considering when the table of some of the steps " \
    "is longer than the remaining things"

    feature = Feature.from_string(FEATURE5)
    assert_equals(feature.max_length, 83)

def test_feature_max_length_on_step_with_table_keys():
    "The max length of a feature considering when the table keys of some of the " \
    "steps are longer than the remaining things"

    feature = Feature.from_string(FEATURE7)
    assert_equals(feature.max_length, 74)

def test_feature_max_length_on_scenario_outline():
    "The max length of a feature considering when the table of some of the  " \
    "scenario oulines is longer than the remaining things"

    feature = Feature.from_string(FEATURE6)
    assert_equals(feature.max_length, 79)

def test_feature_max_length_on_scenario_outline_keys():
    "The max length of a feature considering when the table keys of the  " \
    "scenario oulines are longer than the remaining things"

    feature1 = Feature.from_string(FEATURE8)
    feature2 = Feature.from_string(FEATURE9)
    assert_equals(feature1.max_length, 68)
    assert_equals(feature2.max_length, 68)


def test_description_on_long_named_feature():
    "Can parse the description on long named features"
    feature = Feature.from_string(FEATURE3)
    assert_equals(
        feature.description,
        "In order to describe my features\n"
        "I want to add description on them",
    )


def test_description_on_big_sentenced_steps():
    "Can parse the description on long sentenced steps"
    feature = Feature.from_string(FEATURE4)
    assert_equals(
        feature.description,
        "As a clever guy\n"
        "I want to describe this Feature\n"
        "So that I can take care of my Scenario",
    )


def test_comments():
    "It should ignore lines that start with #, despite white spaces"
    feature = Feature.from_string(FEATURE10)

    assert_equals(feature.max_length, 55)


def test_single_scenario_single_scenario():
    "Features should have at least the first scenario parsed with tags"
    feature = Feature.from_string(FEATURE11)

    first_scenario = feature.scenarios[0]

    assert that(first_scenario.tags).deep_equals([
        'many', 'other', 'basic', 'tags', 'here', ':)'])


def test_single_scenario_many_scenarios():
    "Untagged scenario following a tagged one should have no tags"

    @step('this scenario has tags')
    def scenario_has_tags(step):
        assert step.scenario.tags

    @step('this scenario has no tags')
    def scenario_has_no_tags(step):
        assert not step.scenario.tags

    @step('it can be inspected from within the object')
    def inspected_within_object(step):
        assert step.scenario.tags

    @step(r'fill my email with [\'"]?([^\'"]+)[\'"]?')
    def fill_email(step, email):
        assert that(email).equals('gabriel@lettuce.it')

    feature = Feature.from_string(FEATURE13)

    first_scenario = feature.scenarios[0]
    assert that(first_scenario.tags).equals(['runme'])

    second_scenario = feature.scenarios[1]
    assert that(second_scenario.tags).equals([])

    third_scenario = feature.scenarios[2]
    assert that(third_scenario.tags).equals(['slow'])

    last_scenario = feature.scenarios[3]
    assert that(last_scenario.tags).equals([])

    result = feature.run()
    print
    print
    for sr in result.scenario_results:
        for failed in sr.steps_failed:
            print "+" * 10
            print
            print failed.why.cause
            print
            print "+" * 10

    print
    print
    assert result.passed


def test_scenarios_with_extra_whitespace():
    "Make sure that extra leading whitespace is ignored"
    feature = Feature.from_string(FEATURE14)

    assert_equals(type(feature.scenarios), list)
    assert_equals(len(feature.scenarios), 1, "It should have 1 scenario")
    assert_equals(feature.name, "Extra whitespace feature")

    scenario = feature.scenarios[0]
    assert_equals(type(scenario), Scenario)
    assert_equals(scenario.name, "Extra whitespace scenario")


def test_scenarios_parsing():
    "Tags are parsed correctly"
    feature = Feature.from_string(FEATURE15)
    scenarios_and_tags = [(s.name, s.tags) for s in feature.scenarios]

    scenarios_and_tags.should.equal([
        ('Bootstraping Redis role', []),
        ('Restart scalarizr', []),
        ('Rebundle server', [u'rebundle']),
        ('Use new role', [u'rebundle']),
        ('Restart scalarizr after bundling', [u'rebundle']),
        ('Bundling data', []),
        ('Modifying data', []),
        ('Reboot server', []),
        ('Backuping data on Master', []),
        ('Setup replication', []),
        ('Restart scalarizr in slave', []),
        ('Slave force termination', []),
        ('Slave delete EBS', [u'ec2']),
        ('Setup replication for EBS test', [u'ec2']),
        ('Writing on Master, reading on Slave', []),
        ('Slave -> Master promotion', []),
        ('Restart farm', [u'restart_farm']),
    ])


def test_background_parsing_with_mmf():
    feature = Feature.from_string(FEATURE16)
    expect(feature.description).to.equal(
        "As a rental store owner\n"
        "I want to keep track of my clients\n"
        "So that I can manage my business better"
    )

    expect(feature).to.have.property('background').being.a(Background)
    expect(feature.background).to.have.property('steps')
    expect(feature.background.steps).to.have.length_of(2)

    step1, step2 = feature.background.steps
    step1.sentence.should.equal(
        'Given I have the following movies in my database:')
    step1.hashes.should.equal(HashList(step1, [
        {
            u'Available': u'6',
            u'Rating': u'4 stars',
            u'Name': u'Matrix Revolutions',
            u'New': u'no',
        },
        {
            u'Available': u'11',
            u'Rating': u'5 stars',
            u'Name': u'Iron Man 2',
            u'New': u'yes',
        },
    ]))

    step2.sentence.should.equal(
        'And the following clients:')
    step2.hashes.should.equal(HashList(step2, [
        {u'Name': u'John Doe'},
        {u'Name': u'Foo Bar'},
    ]))


def test_background_parsing_without_mmf():
    feature = Feature.from_string(FEATURE17)
    expect(feature.description).to.be.empty

    expect(feature).to.have.property('background').being.a(Background)
    expect(feature.background).to.have.property('steps')
    expect(feature.background.steps).to.have.length_of(2)

    step1, step2 = feature.background.steps
    step1.sentence.should.equal(
        'Given I have the following movies in my database:')
    step1.hashes.should.equal(HashList(step1, [
        {
            u'Available': u'6',
            u'Rating': u'4 stars',
            u'Name': u'Matrix Revolutions',
            u'New': u'no',
        },
        {
            u'Available': u'11',
            u'Rating': u'5 stars',
            u'Name': u'Iron Man 2',
            u'New': u'yes',
        },
    ]))

    step2.sentence.should.equal(
        'And the following clients:')
    step2.hashes.should.equal(HashList(step2, [
        {u'Name': u'John Doe'},
        {u'Name': u'Foo Bar'},
    ]))


def test_syntax_error_for_scenarios_with_no_name():
    ("Trying to parse features with unnamed "
     "scenarios will cause a syntax error")
    expect(Feature.from_string).when.called_with(FEATURE18).to.throw(
        LettuceSyntaxError,
        ('In the feature "My scenarios have no name", '
         'scenarios must have a name, make sure to declare '
         'a scenario like this: `Scenario: name of your scenario`')
    )
