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
from lettuce.core import STEP_REGISTRY

def _is_step_sentence(sentence):
    return isinstance(sentence, str) or isinstance(sentence, basestring)

def step(step_func_or_sentence):
    """Decorates a function, so that it will become a new step
    definition.
    You give step sentence either (by priority):
    * with step function argument (first example)
    * with function doc (second example)
    * with the function name exploded by underscores (third example)

    Example::

        >>> from lettuce import step
        >>> from models import contact
        >>>
        >>> # First Example
        >>> step(r'Given I delete the contact "(?P<name>.*)" from my address book')
        ... def given_i_do_something(step, name):
        ...     contact.delete_by_name(name)
        ...     assert step.sentence == 'Given I delete the contact "John Doe" from my address book'
        ...
        >>> # Second Example
        >>> @step
        ... def given_i_delete_a_contact_from_my_address_book(step, name):
        ...     '''Given I delete the contact "(?P<name>.*)" from my address book'''
        ...     contact.delete_by_name(name)
        ...     assert step.sentence == 'Given I delete the contact "(?P<name>.*)" from my address book'
        ...
        >>> # Third Example
        >>> @step
        ... def given_I_delete_the_contact_John_Doe_from_my_address_book(step):
        ...     contact.delete_by_name("John Doe")
        ...     assert step.sentence == 'Given I delete the contact John Doe from my address book'


    Notice that all step definitions take a step object as argument.
    """
    if _is_step_sentence(step_func_or_sentence):
        return lambda func: STEP_REGISTRY.load(step_func_or_sentence, func)
    else:
        return STEP_REGISTRY.load_func(step_func_or_sentence)

def steps(steps_class):
    """Decorates a class, and set steps definitions from methods
    except those in the attribute "exclude" or starting by underscore.
    Steps sentences are taken from methods names or docs if exist.

    Example::

        >>> from lettuce import steps
        >>> from models import contact
        >>>
        >>> @steps
        >>> class ListOfSteps(object):
        ...      exclude = ["delete_by_name"]
        ...
        ...      def __init__(self, contact):
        ...          self.contact = contact
        ...
        ...      def given_i_delete_a_contact_from_my_address_book(self, step, name):
        ...          '''Given I delete the contact "(?P<name>.*)" from my address book'''
        ...          self.delete_by_name(name)
        ...          assert step.sentence == 'Given I delete the contact "(?P<name>.*)" from my address book'
        ...
        ...      def given_I_delete_the_contact_John_Doe_from_my_address_book(self, step):
        ...          self.delete_by_name("John Doe")
        ...          assert step.sentence == 'Given I delete the contact John Doe from my address book'
        ...
        ...      def delete_by_name(self, name):
        ...          self.contact.delete_by_name(name)
        ...
        >>> ListOfSteps(contact)


    Notice steps are added when an object of the class is created.
    """
    if hasattr(steps_class, '__init__'):
        _init_ = getattr(steps_class, '__init__')
        def init(self, *args, **kwargs):
            _init_(self, *args, **kwargs)
            STEP_REGISTRY.load_steps(self)
    else:
        def init(self, *args, **kwargs):
            STEP_REGISTRY.load_steps(self)

    setattr(steps_class, '__init__', init)
    return steps_class
