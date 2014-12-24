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
from lettuce.core import Language

def test_language_is_english_by_default():
    "Language class is english by default"
    lang = Language()

    assert_equals(lang.code, 'en')
    assert_equals(lang.name, 'English')
    assert_equals(lang.native, 'English')
    assert_equals(lang.feature, 'Feature')
    assert_equals(lang.scenario, 'Scenario')
    assert_equals(lang.examples, 'Examples|Scenarios')
    assert_equals(lang.scenario_outline, 'Scenario Outline')

def test_language_has_first_of():
    "Language() can pick up first occurrece of a string"
    lang = Language()

    assert_equals(lang.first_of_examples, 'Examples')

def test_search_language_only_in_comments():
    assert_equals(Language.guess_from_string('#  language: fr').code, 'fr') 
    assert_equals(Language.guess_from_string('#language: fr  ').code, 'fr') 
    assert_equals(Language.guess_from_string('  #language:   fr').code, 'fr') 
    assert_equals(Language.guess_from_string(' #   language: fr').code, 'fr') 
    assert_equals(Language.guess_from_string('\t#   language: fr').code, 'fr') 
    assert_equals(Language.guess_from_string('# language: fr foo').code, 'fr') 
    
    assert_equals(Language.guess_from_string('language: fr').code, 'en') 
    assert_equals(Language.guess_from_string('#And my current language: fr').code, 'en') 
