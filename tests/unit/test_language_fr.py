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
from nose.tools import assert_equals
from lettuce.core import Language, Scenario, Feature

SCENARIO = u"""
Scénario: Ajout de plusieurs cursus dans la base de mon université
    Soit Une liste de cursus disponibles dans mon université
        | Nom                       | Durée    |
        | Science de l'Informatique | 5 ans    |
        | Nutrition                 | 4 ans    |
    Quand je consolide la base dans 'cursus.txt'
    Alors je vois que la 1er ligne de 'cursus.txt' contient 'Science de l'Informatique:5
    Et je vois que la 2em ligne de 'cursus.txt' contient 'Nutrition:4'
"""

OUTLINED_SCENARIO = u"""
Plan de Scénario: Ajouter 2 nombres
    Soit <input_1> entré dans la calculatrice
    Et <input_2> entré dans la calculatrice
    Quand je presse <bouton>
    Alors je doit avoir <output> à l'écran

    Exemples:
      | input_1 | input_2 | bouton | output |
      | 20      | 30      | add    | 50     |
      | 2       | 5       | add    | 7      |
      | 0       | 40      | add    | 40     |
"""

OUTLINED_SCENARIO2 = u"""
Plan de Scénario: Ajouter 2 nombres
    Soit <input_1> entré dans la calculatrice
    Et <input_2> entré dans la calculatrice
    Quand je presse <bouton>
    Alors je doit avoir <output> à l'écran

    Scénarios:
      | input_1 | input_2 | bouton | output |
      | 20      | 30      | add    | 50     |
      | 2       | 5       | add    | 7      |
      | 0       | 40      | add    | 40     |
"""
OUTLINED_SCENARIO3 = u"""
Plan du Scénario: Ajouter 2 nombres
    Soit <input_1> entré dans la calculatrice
    Et <input_2> entré dans la calculatrice
    Quand je presse <bouton>
    Alors je doit avoir <output> à l'écran

    Scénarios:
      | input_1 | input_2 | bouton | output |
      | 20      | 30      | add    | 50     |
      | 2       | 5       | add    | 7      |
      | 0       | 40      | add    | 40     |
"""

OUTLINED_FEATURE = u"""
Fonctionnalité: Faire plusieur choses en même temps
    De façon à automatiser les tests
    En tant que fainéant
    J'utilise les plans de scénario

    Plan de Scénario: Ajouter 2 nombres
        Soit <input_1> entré dans la calculatrice
        Et <input_2> entré dans la calculatrice
        Quand je presse <bouton>
        Alors je doit avoir <output> à l'écran

    Exemples:
        | input_1 | input_2 | bouton | output |
        | 20      | 30      | add    | 50     |
        | 2       | 5       | add    | 7      |
        | 0       | 40      | add    | 40     |
"""
OUTLINED_FEATURE2 = u"""
Fonction: Faire plusieur choses en même temps
    De façon à automatiser les tests
    En tant que fainéant
    J'utilise les plans de scénario

    Plan de Scénario: Ajouter 2 nombres
        Soit <input_1> entré dans la calculatrice
        Et <input_2> entré dans la calculatrice
        Quand je presse <bouton>
        Alors je doit avoir <output> à l'écran

    Exemples:
        | input_1 | input_2 | bouton | output |
        | 20      | 30      | add    | 50     |
        | 2       | 5       | add    | 7      |
        | 0       | 40      | add    | 40     |
"""

def test_language_french():
    'Language: FR -> Language class supports french through code "fr"'
    lang = Language('fr')

    assert_equals(lang.code, u'fr')
    assert_equals(lang.name, u'French')
    assert_equals(lang.native, u'Français')
    assert_equals(lang.feature, u'Fonctionnalité|Fonction')
    assert_equals(lang.scenario, u'Scénario')
    assert_equals(lang.examples, u'Exemples|Scénarios')
    assert_equals(lang.scenario_outline, u'Plan de Scénario|Plan du Scénario')
    assert_equals(lang.scenario_separator, u'(Plan de Scénario|Plan du Scénario|Scénario)')

def test_scenario_fr_from_string():
    'Language: FR -> Scenario.from_string'
    lang = Language('fr')
    scenario = Scenario.from_string(SCENARIO, language=lang)

    assert_equals(
        scenario.name,
        u'Ajout de plusieurs cursus dans la base de mon université'
    )
    assert_equals(
        scenario.steps[0].hashes,
        [
            {'Nom': u"Science de l'Informatique", u'Durée': '5 ans'},
            {'Nom': u'Nutrition', u'Durée': '4 ans'},
        ]
    )

def test_scenario_outline1_fr_from_string():
    'Language: FR -> Scenario.from_string, with scenario outline, first case'
    lang = Language('fr')
    scenario = Scenario.from_string(OUTLINED_SCENARIO, language=lang)

    assert_equals(
        scenario.name,
        'Ajouter 2 nombres'
    )
    assert_equals(
        scenario.outlines,
        [
            {u'input_1':u'20',u'input_2':u'30',u'bouton':u'add',u'output':u'50'},
            {u'input_1':u'2',u'input_2':u'5',u'bouton':u'add',u'output':u'7'},
            {u'input_1':u'0',u'input_2':u'40',u'bouton':u'add',u'output':u'40'},
        ]
    )

def test_scenario_outline2_fr_from_string():
    'Language: FR -> Scenario.from_string, with scenario outline, second case'
    lang = Language('fr')
    scenario = Scenario.from_string(OUTLINED_SCENARIO2, language=lang)

    assert_equals(
        scenario.name,
        'Ajouter 2 nombres'
    )
    assert_equals(
        scenario.outlines,
        [
            {u'input_1':u'20',u'input_2':u'30',u'bouton':u'add',u'output':u'50'},
            {u'input_1':u'2',u'input_2':u'5',u'bouton':u'add',u'output':u'7'},
            {u'input_1':u'0',u'input_2':u'40',u'bouton':u'add',u'output':u'40'},
        ]
    )
def test_scenario_outline3_fr_from_string():
    'Language: FR -> Scenario.from_string, with scenario outline, third case'
    lang = Language('fr')
    scenario = Scenario.from_string(OUTLINED_SCENARIO2, language=lang)

    assert_equals(
        scenario.name,
        'Ajouter 2 nombres'
    )
    assert_equals(
        scenario.outlines,
        [
            {u'input_1':u'20',u'input_2':u'30',u'bouton':u'add',u'output':u'50'},
            {u'input_1':u'2',u'input_2':u'5',u'bouton':u'add',u'output':u'7'},
            {u'input_1':u'0',u'input_2':u'40',u'bouton':u'add',u'output':u'40'},
        ]
    )

def test_feature_fr_from_string():
    'Language: FR -> Feature.from_string'
    lang = Language('fr')

    feature = Feature.from_string(OUTLINED_FEATURE, language=lang)

    assert_equals(
        feature.name,
        u'Faire plusieur choses en même temps'
    )

    assert_equals(
        feature.description,
        u"De façon à automatiser les tests\n"
        u"En tant que fainéant\n"
        u"J'utilise les plans de scénario"
    )

    (scenario, ) = feature.scenarios

    assert_equals(
        scenario.name,
        'Ajouter 2 nombres'
    )

    assert_equals(
        scenario.outlines,
        [
            {u'input_1':u'20',u'input_2':u'30',u'bouton':u'add',u'output':u'50'},
            {u'input_1':u'2',u'input_2':u'5',u'bouton':u'add',u'output':u'7'},
            {u'input_1':u'0',u'input_2':u'40',u'bouton':u'add',u'output':u'40'},
        ]
    )
def test_feature_fr_from_string2():
    'Language: FR -> Feature.from_string, alternate name'
    lang = Language('fr')

    feature = Feature.from_string(OUTLINED_FEATURE2, language=lang)

    assert_equals(
        feature.name,
        u'Faire plusieur choses en même temps'
    )

    assert_equals(
        feature.description,
        u"De façon à automatiser les tests\n"
        u"En tant que fainéant\n"
        u"J'utilise les plans de scénario"
    )

    (scenario, ) = feature.scenarios

    assert_equals(
        scenario.name,
        'Ajouter 2 nombres'
    )

    assert_equals(
        scenario.outlines,
        [
            {u'input_1':u'20',u'input_2':u'30',u'bouton':u'add',u'output':u'50'},
            {u'input_1':u'2',u'input_2':u'5',u'bouton':u'add',u'output':u'7'},
            {u'input_1':u'0',u'input_2':u'40',u'bouton':u'add',u'output':u'40'},
        ]
    )
