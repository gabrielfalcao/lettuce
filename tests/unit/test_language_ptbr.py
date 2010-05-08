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
from nose.tools import assert_equals
from lettuce.core import Language

def test_language_portuguese():
    'Language class supports portuguese through code "pt-br"'
    lang = Language('pt-br')

    assert_equals(lang.code, 'pt-br')
    assert_equals(lang.name, 'Portuguese')
    assert_equals(lang.native, u'Português')
    assert_equals(lang.feature, 'Funcionalidade')
    assert_equals(lang.scenario, u'Cenário|Cenario')
    assert_equals(lang.examples, 'Exemplos|Cenários')
    assert_equals(lang.scenario_outline, 'Esquema do Cenário|Esquema do Cenario')
