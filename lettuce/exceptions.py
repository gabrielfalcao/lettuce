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
import traceback
import sys
from lettuce.strings import utf8_string


class NoDefinitionFound(Exception):
    """ Exception raised by lettuce.core.Step, when trying to solve a
    Step, but does not find a suitable step definition.

    This exception should never blow on user's face. It used merely yo
    lettuce can filter undefined steps.
    """
    def __init__(self, step):
        self.step = step

        error = filter(lambda x : 0 <= ord(x) <= 127,
                       'The step r"%s" is not defined' % self.step.sentence)
        super(NoDefinitionFound, self).__init__(error)



class ReasonToFail(object):
    """ Exception that contains detailed information about a
    AssertionError raised within a step definition.  With these data
    lettuce show detailed traceback to user in a nice representation.
    """
    def __init__(self, step, exc):
        self.step = step
        self.exception = exc

        if sys.version_info[:2] < (2, 6):
            msg = exc.message
        else:
            msg = exc.args[0] if exc.args else ''

        if isinstance(msg, basestring):
            self.cause = utf8_string(msg)
        self.traceback = utf8_string(traceback.format_exc(exc))


class LettuceSyntaxError(SyntaxError):
    def __init__(self, filename, string):
        self.filename = filename
        self.msg = "Syntax error at: %s\n%s\n" % (filename, string)


class StepLoadingError(Exception):
    """Raised when a step cannot be loaded."""
    pass
