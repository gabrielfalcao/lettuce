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
from os.path import dirname, abspath, join
from nose.tools import with_setup
from tests.asserts import prepare_stdout
from tests.asserts import assert_stdout_lines

from lettuce import Runner

current_dir = abspath(dirname(__file__))
join_path = lambda *x: join(current_dir, *x)

@with_setup(prepare_stdout)
def test_output_with_success_colorless():
    "Language: ru -> sucess colorless"

    runner = Runner(join_path('ru', 'success', 'dumb.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'Функционал: тупая фича                # tests/functional/language_specific_features/ru/success/dumb.feature:3\n'
        u'  Чтобы lettuce был более надежным    # tests/functional/language_specific_features/ru/success/dumb.feature:4\n'
        u'  Как программист                     # tests/functional/language_specific_features/ru/success/dumb.feature:5\n'
        u'  Я хочу что бы тест был зеленый      # tests/functional/language_specific_features/ru/success/dumb.feature:6\n'
        u'\n'
        u'  Сценарий: Ничего не делать          # tests/functional/language_specific_features/ru/success/dumb.feature:8\n'
        u'    Пуская я ничего не делаю          # tests/functional/language_specific_features/ru/success/dumb_steps.py:6\n'
        u'    Тогда я вижу что тест выполняется # tests/functional/language_specific_features/ru/success/dumb_steps.py:10\n'
        u'\n'
        u'1 feature (1 passed)\n'
        u'1 scenario (1 passed)\n'
        u'2 steps (2 passed)\n'
    )

@with_setup(prepare_stdout)
def test_output_of_table_with_success_colorless():
    "Language: ru -> sucess table colorless"

    runner = Runner(join_path('ru', 'success', 'table.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u"\n"
        u"Функционал: фича с табличкой                                     # tests/functional/language_specific_features/ru/success/table.feature:3\n"
        u"  Для того, что бы lettuce был надежным                          # tests/functional/language_specific_features/ru/success/table.feature:4\n"
        u"  Как программист                                                # tests/functional/language_specific_features/ru/success/table.feature:5\n"
        u"  Я хочу, что бы тесты с таблицами работали отлично и на русском # tests/functional/language_specific_features/ru/success/table.feature:6\n"
        u"\n"
        u"  Сценарий: Проверить таблички                                   # tests/functional/language_specific_features/ru/success/table.feature:8\n"
        u"    Пускай имеем таблицу пациентов:                              # tests/functional/language_specific_features/ru/success/table_steps.py:5\n"
        u"      | ФИО        | Диагноз             |\n"
        u"      | Петров ПП  | диарея              |\n"
        u"      | Сидоров НА | хронический снобизм |\n"
        u"\n"
        u"1 feature (1 passed)\n"
        u"1 scenario (1 passed)\n"
        u"1 step (1 passed)\n"
    )

@with_setup(prepare_stdout)
def test_output_outlines_success_colorless():
    "Language: ru -> sucess outlines colorless"

    runner = Runner(join_path('ru', 'success', 'outlines.feature'), verbosity=3, no_color=True)
    runner.run()

    assert_stdout_lines(
        u'\n'
        u'Функционал: Проверить вывод структурного сценария                                  # tests/functional/language_specific_features/ru/success/outlines.feature:3\n'
        u'  Как программист                                                                  # tests/functional/language_specific_features/ru/success/outlines.feature:4\n'
        u'  Для того чобы lettuce был надежным                                               # tests/functional/language_specific_features/ru/success/outlines.feature:5\n'
        u'  Я хочу, что бы сценарии со структурой работали на русском                        # tests/functional/language_specific_features/ru/success/outlines.feature:6\n'
        u'\n'
        u'  Структура сценария: Заполнить форму                                              # tests/functional/language_specific_features/ru/success/outlines.feature:8\n'
        u'    Пускай я открываю в браузере  "http://sona-studio.com/contacts/"               # tests/functional/language_specific_features/ru/success/outlines_steps.py:12\n'
        u'    Когда я заполняю в поле "Имя" "<имя>"                                          # tests/functional/language_specific_features/ru/success/outlines_steps.py:16\n'
        u'    И я заполняю в поле "Email" "<email>"                                          # tests/functional/language_specific_features/ru/success/outlines_steps.py:24\n'
        u'    И я заполняю в поле "Сообщение" "<сообщение>"                                  # tests/functional/language_specific_features/ru/success/outlines_steps.py:32\n'
        u'    И я нажимаю "Отправить"                                                        # tests/functional/language_specific_features/ru/success/outlines_steps.py:40\n'
        u'    Тогда я получаю сообщение "Спасибо за ваше сообщение"                          # tests/functional/language_specific_features/ru/success/outlines_steps.py:43\n'
        u'\n'
        u'  Примеры:\n'
        u'    | имя              | email          | сообщение                              |\n'
        u'    | Виталий Игоревич | john@gmail.org | Есть интересный проект, нужно обсудить |\n'
        u'    | Марина Банраул   | mary@email.com | Мне нравятся ваши дизайны, хочу сайт   |\n'
        u'\n'
        u'1 feature (1 passed)\n'
        u'2 scenarios (2 passed)\n'
        u'12 steps (12 passed)\n'
    )

@with_setup(prepare_stdout)
def test_output_outlines_success_colorful():
    "Language: ru -> sucess outlines colorful"

    runner = Runner(join_path('ru', 'success', 'outlines.feature'), verbosity=3, no_color=False)
    runner.run()

    assert_stdout_lines(
        u'\n'
u'\x1b[1;37m\u0424\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b: \u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u0432\u044b\u0432\u043e\u0434 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u043d\u043e\u0433\u043e \u0441\u0446\u0435\u043d\u0430\u0440\u0438\u044f                                  \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines.feature:3\x1b[0m\n'
u'\x1b[1;37m  \u041a\u0430\u043a \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0441\u0442                                                                  \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines.feature:4\x1b[0m\n'
u'\x1b[1;37m  \u0414\u043b\u044f \u0442\u043e\u0433\u043e \u0447\u043e\u0431\u044b lettuce \u0431\u044b\u043b \u043d\u0430\u0434\u0435\u0436\u043d\u044b\u043c                                               \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines.feature:5\x1b[0m\n'
u'\x1b[1;37m  \u042f \u0445\u043e\u0447\u0443, \u0447\u0442\u043e \u0431\u044b \u0441\u0446\u0435\u043d\u0430\u0440\u0438\u0438 \u0441\u043e \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u043e\u0439 \u0440\u0430\u0431\u043e\u0442\u0430\u043b\u0438 \u043d\u0430 \u0440\u0443\u0441\u0441\u043a\u043e\u043c                        \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines.feature:6\x1b[0m\n'
u'\n'
u'\x1b[1;37m  \u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u0441\u0446\u0435\u043d\u0430\u0440\u0438\u044f: \u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0444\u043e\u0440\u043c\u0443                                              \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines.feature:8\x1b[0m\n'
u'\x1b[0;36m    \u041f\u0443\u0441\u043a\u0430\u0439 \u044f \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u044e \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0435  "http://sona-studio.com/contacts/"               \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines_steps.py:12\x1b[0m\n'
u'\x1b[0;36m    \u041a\u043e\u0433\u0434\u0430 \u044f \u0437\u0430\u043f\u043e\u043b\u043d\u044f\u044e \u0432 \u043f\u043e\u043b\u0435 "\u0418\u043c\u044f" "<\u0438\u043c\u044f>"                                          \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines_steps.py:16\x1b[0m\n'
u'\x1b[0;36m    \u0418 \u044f \u0437\u0430\u043f\u043e\u043b\u043d\u044f\u044e \u0432 \u043f\u043e\u043b\u0435 "Email" "<email>"                                          \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines_steps.py:24\x1b[0m\n'
u'\x1b[0;36m    \u0418 \u044f \u0437\u0430\u043f\u043e\u043b\u043d\u044f\u044e \u0432 \u043f\u043e\u043b\u0435 "\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435" "<\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435>"                                  \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines_steps.py:32\x1b[0m\n'
u'\x1b[0;36m    \u0418 \u044f \u043d\u0430\u0436\u0438\u043c\u0430\u044e "\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c"                                                        \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines_steps.py:40\x1b[0m\n'
u'\x1b[0;36m    \u0422\u043e\u0433\u0434\u0430 \u044f \u043f\u043e\u043b\u0443\u0447\u0430\u044e \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 "\u0421\u043f\u0430\u0441\u0438\u0431\u043e \u0437\u0430 \u0432\u0430\u0448\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435"                          \x1b[1;30m# tests/functional/language_specific_features/ru/success/outlines_steps.py:43\x1b[0m\n'
u'\n'
u'\x1b[1;37m  \u041f\u0440\u0438\u043c\u0435\u0440\u044b:\x1b[0m\n'
u'\x1b[0;36m   \x1b[1;37m |\x1b[0;36m \u0438\u043c\u044f             \x1b[1;37m |\x1b[0;36m email         \x1b[1;37m |\x1b[0;36m \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435                             \x1b[1;37m |\x1b[0;36m\x1b[0m\n'
u'\x1b[1;32m   \x1b[1;37m |\x1b[1;32m \u0412\u0438\u0442\u0430\u043b\u0438\u0439 \u0418\u0433\u043e\u0440\u0435\u0432\u0438\u0447\x1b[1;37m |\x1b[1;32m john@gmail.org\x1b[1;37m |\x1b[1;32m \u0415\u0441\u0442\u044c \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043d\u044b\u0439 \u043f\u0440\u043e\u0435\u043a\u0442, \u043d\u0443\u0436\u043d\u043e \u043e\u0431\u0441\u0443\u0434\u0438\u0442\u044c\x1b[1;37m |\x1b[1;32m\x1b[0m\n'
u'\x1b[1;32m   \x1b[1;37m |\x1b[1;32m \u041c\u0430\u0440\u0438\u043d\u0430 \u0411\u0430\u043d\u0440\u0430\u0443\u043b  \x1b[1;37m |\x1b[1;32m mary@email.com\x1b[1;37m |\x1b[1;32m \u041c\u043d\u0435 \u043d\u0440\u0430\u0432\u044f\u0442\u0441\u044f \u0432\u0430\u0448\u0438 \u0434\u0438\u0437\u0430\u0439\u043d\u044b, \u0445\u043e\u0447\u0443 \u0441\u0430\u0439\u0442  \x1b[1;37m |\x1b[1;32m\x1b[0m\n'
u'\n'
u'\x1b[1;37m1 feature (\x1b[1;32m1 passed\x1b[1;37m)\x1b[0m\n'
u'\x1b[1;37m2 scenarios (\x1b[1;32m2 passed\x1b[1;37m)\x1b[0m\n'
u'\x1b[1;37m12 steps (\x1b[1;32m12 passed\x1b[1;37m)\x1b[0m\n'
    )

