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
    "Language: pt-br -> sucess colorless"

    runner = Runner(join_path('pt-br', 'success', 'dumb.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u"\n"
        u"Funcionalidade: feature burra       # tests/functional/language_specific_features/pt-br/success/dumb.feature:3\n"
        u"  Como um programador               # tests/functional/language_specific_features/pt-br/success/dumb.feature:4\n"
        u"  Eu quero que este teste passe     # tests/functional/language_specific_features/pt-br/success/dumb.feature:5\n"
        u"  Para testar um cenário de sucesso # tests/functional/language_specific_features/pt-br/success/dumb.feature:6\n"
        u"\n"
        u"  Cenário: Fazer nada               # tests/functional/language_specific_features/pt-br/success/dumb.feature:8\n"
        u"    Dado que eu faço nada           # tests/functional/language_specific_features/pt-br/success/dumb_steps.py:6\n"
        u"\n"
        u"1 feature (1 passed)\n"
        u"1 scenario (1 passed)\n"
        u"1 step (1 passed)\n"
    )

@with_setup(prepare_stdout)
def test_output_of_table_with_success_colorless():
    "Language: pt-br -> sucess table colorless"

    runner = Runner(join_path('pt-br', 'success', 'table.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u"\n"
        u"Funcionalidade: feature burra, com tabela      # tests/functional/language_specific_features/pt-br/success/table.feature:3\n"
        u"  Como um programador                          # tests/functional/language_specific_features/pt-br/success/table.feature:4\n"
        u"  Eu quero testar steps com tabelas            # tests/functional/language_specific_features/pt-br/success/table.feature:5\n"
        u"  Para ver o output em pt-br                   # tests/functional/language_specific_features/pt-br/success/table.feature:6\n"
        u"\n"
        u"  Cenário: Fazer nada, com tabelas :)          # tests/functional/language_specific_features/pt-br/success/table.feature:8\n"
        u"    Dado que eu brinco com os seguintes itens: # tests/functional/language_specific_features/pt-br/success/table_steps.py:6\n"
        u"      | id | description  |\n"
        u"      | 12 | some desc    |\n"
        u"      | 64 | another desc |\n"
        u"\n"
        u"1 feature (1 passed)\n"
        u"1 scenario (1 passed)\n"
        u"1 step (1 passed)\n"
    )

@with_setup(prepare_stdout)
def test_output_outlines_success_colorless():
    "Language: pt-br -> sucess outlines colorless"

    runner = Runner(join_path('pt-br', 'success', 'outlines.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'Funcionalidade: outlines em português                                  # tests/functional/language_specific_features/pt-br/success/outlines.feature:3\n'
        u'  Como um programador                                                  # tests/functional/language_specific_features/pt-br/success/outlines.feature:4\n'
        u'  Eu quero testar cenários esquemáticos                                # tests/functional/language_specific_features/pt-br/success/outlines.feature:5\n'
        u'  Para ver o output em pt-br                                           # tests/functional/language_specific_features/pt-br/success/outlines.feature:6\n'
        u'\n'
        u'  Esquema do Cenário: Fazer nada, repetidas vezes, através de esquemas # tests/functional/language_specific_features/pt-br/success/outlines.feature:8\n'
        u'    Dado que tenho o <dado1>                                           # tests/functional/language_specific_features/pt-br/success/outlines_steps.py:13\n'
        u'    Quando eu faço algo com <isso>                                     # tests/functional/language_specific_features/pt-br/success/outlines_steps.py:22\n'
        u'    Então eu fico feliz em ver <aquilo>                                # tests/functional/language_specific_features/pt-br/success/outlines_steps.py:31\n'
        u'\n'
        u'  Exemplos:\n'
        u'    | dado1 | isso        | aquilo        |\n'
        u'    | algo  | assim       | funcional     |\n'
        u'    | outro | aqui        | também        |\n'
        u'    | dados | funcionarão | com unicode ! |\n'
        u'\n'
        u'1 feature (1 passed)\n'
        u'3 scenarios (3 passed)\n'
        u'9 steps (9 passed)\n'
    )

@with_setup(prepare_stdout)
def test_output_outlines_success_colorful():
    "Language: pt-br -> sucess outlines colorful"

    runner = Runner(join_path('pt-br', 'success', 'outlines.feature'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'\033[1;37mFuncionalidade: outlines em português                                  \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines.feature:3\033[0m\n'
        u'\033[1;37m  Como um programador                                                  \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines.feature:4\033[0m\n'
        u'\033[1;37m  Eu quero testar cenários esquemáticos                                \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines.feature:5\033[0m\n'
        u'\033[1;37m  Para ver o output em pt-br                                           \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines.feature:6\033[0m\n'
        u'\n'
        u'\033[1;37m  Esquema do Cenário: Fazer nada, repetidas vezes, através de esquemas \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines.feature:8\033[0m\n'
        u'\033[0;36m    Dado que tenho o <dado1>                                           \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines_steps.py:13\033[0m\n'
        u'\033[0;36m    Quando eu faço algo com <isso>                                     \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines_steps.py:22\033[0m\n'
        u'\033[0;36m    Então eu fico feliz em ver <aquilo>                                \033[1;30m# tests/functional/language_specific_features/pt-br/success/outlines_steps.py:31\033[0m\n'
        u'\n'
        u'\033[1;37m  Exemplos:\033[0m\n'
        u'\033[0;36m   \033[1;37m |\033[0;36m dado1\033[1;37m |\033[0;36m isso       \033[1;37m |\033[0;36m aquilo       \033[1;37m |\033[0;36m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m algo \033[1;37m |\033[1;32m assim      \033[1;37m |\033[1;32m funcional    \033[1;37m |\033[1;32m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m outro\033[1;37m |\033[1;32m aqui       \033[1;37m |\033[1;32m também       \033[1;37m |\033[1;32m\033[0m\n'
        u'\033[1;32m   \033[1;37m |\033[1;32m dados\033[1;37m |\033[1;32m funcionarão\033[1;37m |\033[1;32m com unicode !\033[1;37m |\033[1;32m\033[0m\n'
        u'\n'
        u"\033[1;37m1 feature (\033[1;32m1 passed\033[1;37m)\033[0m\n" \
        u"\033[1;37m3 scenarios (\033[1;32m3 passed\033[1;37m)\033[0m\n" \
        u"\033[1;37m9 steps (\033[1;32m9 passed\033[1;37m)\033[0m\n"
    )

