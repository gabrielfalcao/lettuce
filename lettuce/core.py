# -*- coding: utf-8 -*-
# <Lettuce - Behavior-driven design for python>
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

class Step(object):
    def __init__(self, sentence, keys, data_list):
        self.sentence = sentence
        self.keys = tuple(keys)
        self.data_list = list(data_list)

    @classmethod
    def from_string(cls, string):
        string = string.strip()
        lines = [l.strip() for l in string.splitlines()]
        sentence = lines.pop(0)
        keys = [k.strip() for k in lines.pop(0).split("|") if k]

        data_list = []
        for line in lines:
            values = [k.strip() for k in line.split("|") if k]
            data_list.append(dict(zip(keys, values)))

        return cls(sentence, keys, data_list)
