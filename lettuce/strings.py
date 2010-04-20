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
import re

def escape_if_necessary(what):
    if len(what) is 1:
        what = "[%s]" % what

    return what

def get_stripped_lines(string):
    lines = [l.strip() for l in string.splitlines()]
    return [l for l in lines if l]

def split_wisely(string, sep, strip=False):
    regex = re.compile(escape_if_necessary(sep),  re.I | re.M)

    items = filter(lambda x: x, regex.split(string))
    if strip:
        items = [i.strip() for i in items]
    else:
        items = [i.strip("\n") for i in items]

    return [i for i in items if i]

def wise_startswith(string, seed):
    regex = "^%s" % re.escape(seed)
    return bool(re.search(regex, string, re.I))

def remove_it(string, what):
    return re.sub(what, "", string).strip()
