# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
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
import sys

from StringIO import StringIO

from os.path import dirname, abspath, join
from nose.tools import assert_equals, with_setup

from lettuce import Runner, CALLBACK_REGISTRY

current_dir = abspath(dirname(__file__))
join_path = lambda *x: join(current_dir, *x)

def prepare_stdout():
    CALLBACK_REGISTRY.clear()

    if isinstance(sys.stdout, StringIO):
        del sys.stdout

    std = StringIO()
    sys.stdout = std

def assert_lines(one, other):
    lines_one = one.splitlines()
    lines_other = other.splitlines()

    for line1, line2 in zip(lines_one, lines_other):
        assert_equals(line1, line2)

    assert_equals(len(lines_one), len(lines_other))

def assert_stdout_lines(other):
    one = sys.stdout.getvalue()
    assert_lines(one, other)

@with_setup(prepare_stdout)
def test_output_with_success_colorless():
    "Language: pt-br -> sucess colorless"

    runner = Runner(join_path('pt-br', 'success', 'dumb.feature'), verbosity=3)
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
        u"\033[A    Dado que eu faço nada           # tests/functional/language_specific_features/pt-br/success/dumb_steps.py:6\n"
        u"\n"
        u"1 feature (1 passed)\n"
        u"1 scenario (1 passed)\n"
        u"1 step (1 passed)\n"
    )

@with_setup(prepare_stdout)
def test_output_of_table_with_success_colorless():
    "Language: pt-br -> sucess table colorless"

    runner = Runner(join_path('pt-br', 'success', 'table.feature'), verbosity=3)
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
        u"\033[A\033[A\033[A\033[A    Dado que eu brinco com os seguintes itens: # tests/functional/language_specific_features/pt-br/success/table_steps.py:6\n"
        u"      | id | description  |\n"
        u"      | 12 | some desc    |\n"
        u"      | 64 | another desc |\n"
        u"\n"
        u"1 feature (1 passed)\n"
        u"1 scenario (1 passed)\n"
        u"1 step (1 passed)\n"
    )

