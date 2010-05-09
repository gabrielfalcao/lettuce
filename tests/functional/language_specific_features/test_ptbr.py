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

from language_helper import *

@with_setup(prepare_stdout)
def test_output_with_success_colorless():
    "Testing the colorless output of a successful feature"

    runner = Runner(join_path('pt-br', 'success', 'dumb.feature'), verbosity=3)
    runner.run()

    assert_stdout_lines(
        "\n"
        "Funcionalidade: feature burra       # tests/functional/output_features/runner_features/first.feature:1\n"
        "  In order to test success          # tests/functional/output_features/runner_features/first.feature:2\n"
        "  Eu quero que este teste passe     # tests/functional/output_features/runner_features/first.feature:3\n"
        "  Para testar um cenário de sucesso # tests/functional/output_features/runner_features/first.feature:4\n"
        "\n"
        "  Cenário: Fazer nada               # tests/functional/output_features/runner_features/first.feature:6\n"
        "    Dado que eu faço nada           # tests/functional/output_features/runner_features/dumb_steps.py:6\n"
        "\033[A    Dado que eu faço nada           # tests/functional/output_features/runner_features/dumb_steps.py:6\n"
        "\n"
        "1 feature (1 passed)\n"
        "1 scenario (1 passed)\n"
        "1 step (1 passed)\n"
    )
