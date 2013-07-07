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
# MERsteps.pyCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from cStringIO import StringIO

from lettuce.terrain import before, after

from subunit.v2 import StreamResultToBytes

def open_file(filename):
    """
    open a subunit file

    this is not a context manager because it is used asynchronously by
    hooks
    
    out of the scope of enable() because we want to patch it in our tests
    """

    filename = filename or 'subunit.bin'

    return open(filename, 'wb')


def close_file(file_):
    """
    """

    file_.close()


def enable(filename=None):

    file_ = open_file(filename)

    streamresult = StreamResultToBytes(file_)
    streamresult.startTestRun()

    real_stdout = sys.stdout
    real_stderr = sys.stderr

    @before.each_scenario
    def before_scenario(scenario):

        # redirect stdout and stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        streamresult.status(test_id=get_test_id(scenario),
                            test_status='inprogress')

    @after.each_scenario
    def after_scenario(scenario):

        streamresult.status(test_id=get_test_id(scenario),
                            test_status='inprogress',
                            file_name='stdout',
                            file_bytes=sys.stdout.getvalue(),
                            mime_type='text/plain; charset=utf8',
                            eof=True)

        streamresult.status(test_id=get_test_id(scenario),
                            test_status='inprogress',
                            file_name='stderr',
                            file_bytes=sys.stderr.getvalue(),
                            mime_type='text/plain; charset=utf8',
                            eof=True)

        # unredirect stdout and stderr
        sys.stdout = real_stdout
        sys.stderr = real_stderr

        if scenario.passed:
            streamresult.status(test_id=get_test_id(scenario),
                                test_status='success')
        else:
            streamresult.status(test_id=get_test_id(scenario),
                                test_status='fail')

    @after.all
    def after_all(total):
        streamresult.stopTestRun()
        close_file(file_)


def get_test_id(scenario):
    return '{}: {}'.format(scenario.feature.name, scenario.name)
