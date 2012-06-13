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
import re
from lettuce.core import STEP_REGISTRY, CASTER_REGISTRY
from lettuce.exceptions import CasterLoadingError, StepLoadingError


def caster(regex):
    """Decorates a function that will be responsible for casting
    matched regex into object, leveraging more flexibility on step
    definitions and simplifying the test ecosystem.

    Example::

    >>> from lettuce import step
    >>> from models import Contact
    >>>
    >>> @step.caster(r'the person "(.*)"')
    ... def into_a_contact_object(value):
    ...     return Contact.objects.get(name=value)
    ...
    >>> @step(r'Given the person "(.*)" is erased from my address book')
    ... def given_i_do_something(step, user):
    ...     user.delete()

    Notice the name matched in the regex below being cast into a
    `Contact` object
    """
    def wrap(func):
        try:
            re.compile(regex)
        except re.error, e:
            raise CasterLoadingError("Error when trying to compile:\n"
                                   "  regex: %r\n"
                                   "  for function: %s\n"
                                   "  error: %s" % (regex, func, e))
        CASTER_REGISTRY[regex] = func
        return func

    return wrap


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

step.caster = caster
