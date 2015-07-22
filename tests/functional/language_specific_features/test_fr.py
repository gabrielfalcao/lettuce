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
from os.path import dirname, abspath, join
from nose.tools import with_setup
from tests.asserts import prepare_stdout
from tests.asserts import assert_stdout_lines

from lettuce import Runner

current_dir = abspath(dirname(__file__))
join_path = lambda *x: join(current_dir, *x)

@with_setup(prepare_stdout)
def test_output_with_success_colorless():
    "Language: fr -> sucess colorless"

    runner = Runner(join_path('fr', 'success', 'dumb.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u"\n"
        u"Fonctionnalité: Test complet # tests/functional/language_specific_features/fr/success/dumb.feature:3\n"
        u"  En tant que programmeur    # tests/functional/language_specific_features/fr/success/dumb.feature:4\n"
        u"  Je veux valider les tests  # tests/functional/language_specific_features/fr/success/dumb.feature:5\n"
        u"\n"
        u"  Scénario: On ne fait rien  # tests/functional/language_specific_features/fr/success/dumb.feature:7\n"
        u"    Quand je ne fait rien    # tests/functional/language_specific_features/fr/success/dumb_steps.py:6\n"
        u"\n"
        u"1 feature (1 passed)\n"
        u"1 scenario (1 passed)\n"
        u"1 step (1 passed)\n"
    )

@with_setup(prepare_stdout)
def test_output_of_table_with_success_colorless():
    "Language: fr -> sucess table colorless"

    runner = Runner(join_path('fr', 'success', 'table.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u"\n"
        u"Fonctionnalité: Test des sorties, avec table        # tests/functional/language_specific_features/fr/success/table.feature:4\n"
        u"  En tant que programmeur                           # tests/functional/language_specific_features/fr/success/table.feature:5\n"
        u"  Je veux tester les sorties de scénario avec table # tests/functional/language_specific_features/fr/success/table.feature:6\n"
        u"\n"
        u"  Scénario: NE rien faire, mais avec des tables     # tests/functional/language_specific_features/fr/success/table.feature:8\n"
        u"    Soit les éléments suivant                       # tests/functional/language_specific_features/fr/success/table_steps.py:6\n"
        u"      | id | élément |\n"
        u"      | 50 | Un      |\n"
        u"      | 59 | 42      |\n"
        u"      | 29 | sieste  |\n"
        u"\n"
        u"1 feature (1 passed)\n"
        u"1 scenario (1 passed)\n"
        u"1 step (1 passed)\n"

    )

@with_setup(prepare_stdout)
def test_output_outlines_success_colorless():
    "Language: fr -> sucess outlines colorless"

    runner = Runner(join_path('fr', 'success', 'outlines.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'Fonctionnalité: Plan de scénario en français # tests/functional/language_specific_features/fr/success/outlines.feature:4\n'
        u'  En tant que programmeur                    # tests/functional/language_specific_features/fr/success/outlines.feature:5\n'
        u'  Je veux tester les plans de scénario       # tests/functional/language_specific_features/fr/success/outlines.feature:6\n'
        u'  Et surtout les sorties                     # tests/functional/language_specific_features/fr/success/outlines.feature:7\n'
        u'\n'
        u'  Plan de Scénario: Faire la sieste          # tests/functional/language_specific_features/fr/success/outlines.feature:9\n'
        u'    Soit un après midi de <mois>             # tests/functional/language_specific_features/fr/success/outlines_steps.py:13\n'
        u'    Quand je veux faire la sieste            # tests/functional/language_specific_features/fr/success/outlines_steps.py:22\n'
        u'    Je peux aller <lieux>                    # tests/functional/language_specific_features/fr/success/outlines_steps.py:26\n'
        u'\n'
        u'  Exemples:\n'
        u'    | mois    | lieux              |\n'
        u'    | janvier | près de la cheminé |\n'
        u'    | aôut    | dans le transat    |\n'
        u'    | octobre | dans le canapé     |\n'
        u'\n'
        u'1 feature (1 passed)\n'
        u'3 scenarios (3 passed)\n'
        u'9 steps (9 passed)\n'
    )

@with_setup(prepare_stdout)
def test_output_outlines_success_colorful():
    "Language: fr -> sucess outlines colorful"

    runner = Runner(join_path('fr', 'success', 'outlines.feature'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'\033[1;37mFonctionnalité: Plan de scénario en français \033[1;30m# tests/functional/language_specific_features/fr/success/outlines.feature:4\033[0m\n'
        u'\033[1;37m  En tant que programmeur                    \033[1;30m# tests/functional/language_specific_features/fr/success/outlines.feature:5\033[0m\n'
        u'\033[1;37m  Je veux tester les plans de scénario       \033[1;30m# tests/functional/language_specific_features/fr/success/outlines.feature:6\033[0m\n'
        u'\033[1;37m  Et surtout les sorties                     \033[1;30m# tests/functional/language_specific_features/fr/success/outlines.feature:7\033[0m\n'
        u'\n'
        u'\033[1;37m  Plan de Scénario: Faire la sieste          \033[1;30m# tests/functional/language_specific_features/fr/success/outlines.feature:9\033[0m\n'
        u'\033[0;36m    Soit un après midi de <mois>             \033[1;30m# tests/functional/language_specific_features/fr/success/outlines_steps.py:13\033[0m\n'
        u'\033[0;36m    Quand je veux faire la sieste            \033[1;30m# tests/functional/language_specific_features/fr/success/outlines_steps.py:22\033[0m\n'
        u'\033[0;36m    Je peux aller <lieux>                    \033[1;30m# tests/functional/language_specific_features/fr/success/outlines_steps.py:26\033[0m\n'
        u'\n'
        u'\033[1;37m  Exemples:\033[0m\n'
        u'\033[0;36m   \033[1;37m |\033[0;36m mois   \033[1;37m |\033[0;36m lieux             \033[1;37m |\033[0;36m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m janvier\033[1;37m |\033[1;32m près de la cheminé\033[1;37m |\033[1;32m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m aôut   \033[1;37m |\033[1;32m dans le transat   \033[1;37m |\033[1;32m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m octobre\033[1;37m |\033[1;32m dans le canapé    \033[1;37m |\033[1;32m\033[0m\n'
        u'\n'
        u'\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n'
        u'\033[1;37m3 scenarios (\033[1;32m3 passed\033[1;37m)\033[0m\n'
        u'\033[1;37m9 steps (\033[1;32m9 passed\033[1;37m)\033[0m\n'
    )
@with_setup(prepare_stdout)
def test_output_outlines2_success_colorful():
    "Language: fr -> sucess outlines colorful, alternate name"

    runner = Runner(join_path('fr', 'success', 'outlines2.feature'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'\033[1;37mFonctionnalité: Plan de scénario en français \033[1;30m# tests/functional/language_specific_features/fr/success/outlines2.feature:4\033[0m\n'
        u'\033[1;37m  En tant que programmeur                    \033[1;30m# tests/functional/language_specific_features/fr/success/outlines2.feature:5\033[0m\n'
        u'\033[1;37m  Je veux tester les plans de scénario       \033[1;30m# tests/functional/language_specific_features/fr/success/outlines2.feature:6\033[0m\n'
        u'\033[1;37m  Et surtout les sorties                     \033[1;30m# tests/functional/language_specific_features/fr/success/outlines2.feature:7\033[0m\n'
        u'\n'
        u'\033[1;37m  Plan de Scénario: Faire la sieste          \033[1;30m# tests/functional/language_specific_features/fr/success/outlines2.feature:9\033[0m\n'
        u'\033[0;36m    Soit un après midi de <mois>             \033[1;30m# tests/functional/language_specific_features/fr/success/outlines_steps.py:13\033[0m\n'
        u'\033[0;36m    Quand je veux faire la sieste            \033[1;30m# tests/functional/language_specific_features/fr/success/outlines_steps.py:22\033[0m\n'
        u'\033[0;36m    Je peux aller <lieux>                    \033[1;30m# tests/functional/language_specific_features/fr/success/outlines_steps.py:26\033[0m\n'
        u'\n'
        u'\033[1;37m  Exemples:\033[0m\n'
        u'\033[0;36m   \033[1;37m |\033[0;36m mois   \033[1;37m |\033[0;36m lieux             \033[1;37m |\033[0;36m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m janvier\033[1;37m |\033[1;32m près de la cheminé\033[1;37m |\033[1;32m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m aôut   \033[1;37m |\033[1;32m dans le transat   \033[1;37m |\033[1;32m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m octobre\033[1;37m |\033[1;32m dans le canapé    \033[1;37m |\033[1;32m\033[0m\n'
        u'\n'
        u'\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n'
        u'\033[1;37m3 scenarios (\033[1;32m3 passed\033[1;37m)\033[0m\n'
        u'\033[1;37m9 steps (\033[1;32m9 passed\033[1;37m)\033[0m\n'
    )
