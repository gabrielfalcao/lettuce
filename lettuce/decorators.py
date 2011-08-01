# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2011>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from lettuce.core import STEP_REGISTRY
from lettuce.exceptions import StepLoadingError


def step(regex):
    """Decorates a function, so that it will become a new step
    definition.

    Example::

        >>> from lettuce import step
        >>> from models import contact
        >>>
        >>> step(r'Given I delete the contact "(?P<name>.*)" from my address book')
        ... def given_i_do_something(step, name):
        ...     contact.delete_by_name(name)
        ...     assert step.sentence == 'Given I delete the contact "John Doe" from my address book'


    Notice that all step definitions take a step object as argument.
    """
    def wrap(func):
        try:
            re.compile(regex)
        except re.error, e:
            raise StepLoadingError("Error when trying to compile:\n"
                                   "  regex: %r\n"
                                   "  for function: %s\n"
                                   "  error: %s" % (regex, func, e))
        STEP_REGISTRY[regex] = func
        return func

    return wrap
