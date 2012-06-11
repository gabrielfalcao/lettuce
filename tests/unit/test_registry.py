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
from lettuce.registry import _function_matches


def test_function_matches_compares_with_abs_path():
    u"lettuce.registry._function_matches() should compare callback filenames with abspath"

    class fakecallback1:
        class func_code:
            co_filename = "/some/path/to/some/../file.py"
            co_firstlineno = 1

    class fakecallback2:
        class func_code:
            co_filename = "/some/path/to/file.py"
            co_firstlineno = 1

    assert _function_matches(fakecallback1, fakecallback2), \
        'the callbacks should have matched'
