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

from cStringIO import StringIO

from nose.tools import with_setup

from lettuce import Runner, registry
from lettuce.plugins import subunit_output
from tests.asserts import prepare_stdout
from tests.functional.test_runner import feature_name

@with_setup(prepare_stdout, registry.clear)
def test_subunit_output():
    """
    Test Subunit output
    """

    output = StringIO()
    patch = (subunit_output.open_file, subunit_output.close_file)

    def close_file(file_):
        print file_.getvalue()
        file_.close()

    subunit_output.open_file = lambda f: output
    subunit_output.close_file = close_file

    runner = Runner(feature_name('commented_feature'), enable_subunit=True)
    runner.run()

    subunit_output.open_file, subunit_output.close_file = patch
