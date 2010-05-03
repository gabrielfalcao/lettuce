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

from lettuce import step

@step(r'Given I open browser at "http://(.*)"')
def given_i_open_browser_at_http_address(step, address):
    pass

@step(r'And click on "sign[-]up"')
def and_click_on_sign_up(step):
    pass

@step(r'I fill the field "(.*)" with "(.*)"')
def when_i_fill_the_field_x_with_y(step, field, value):
    if field == 'password' and value == 'wee-9876':  assert False

@step(r'And I click "done"')
def and_i_click_done(step):
    pass

@step(r'Then I see the message "(.*)"')
def then_i_see_the_message_message(step, message):
    pass
