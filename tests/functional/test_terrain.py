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
from os.path import dirname, abspath, join

from lettuce import Runner
from lettuce.terrain import world

def test_imports_terrain_under_path_that_is_run():

    assert not hasattr(world, 'works_fine')

    runner = Runner(join(abspath(dirname(__file__)), '1st_feature_dir'))
    assert runner.terrain
    assert hasattr(world, 'works_fine')
    assert world.works_fine
