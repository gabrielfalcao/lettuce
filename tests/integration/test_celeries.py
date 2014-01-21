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
import commands
from lettuce.fs import FileSystem
from sure import this as the
from tests.util import in_directory, run_scenario

current_directory = FileSystem.dirname(__file__)


@in_directory(current_directory, 'django', 'celeries')
def test_failfast():
    'passing --failfast to the harvest command will cause lettuce to stop in the first failure'

    status, output = run_scenario(**{'--failfast': None})

    the(output).should.contain("This one is present")
    the(output).should.contain("Celeries before all")
    the(output).should.contain("Celeries before harvest")
    the(output).should.contain("Celeries before feature 'Test the django app leaves'")
    the(output).should.contain("Celeries before scenario 'This one is present'")

    the(output).should.contain("Celeries before step 'Given I say foo bar'")
    the(output).should.contain("Celeries after step 'Given I say foo bar'")
    the(output).should.contain("Celeries before step 'Then it fails'")
    the(output).should.contain("Celeries after step 'Then it fails'")

    the(output).should.contain("Celeries after scenario 'This one is present'")
    the(output).should.contain("Celeries after feature 'Test the django app leaves'")
    the(output).should.contain("Celeries after harvest")
    the(output).should.contain("Celeries after all")

    the(output).should_not.contain("This one is never called")
