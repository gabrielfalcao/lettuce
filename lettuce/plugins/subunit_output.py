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

import datetime
import sys
from StringIO import StringIO

from lettuce.terrain import before, after

from subunit.v2 import StreamResultToBytes
from subunit.iso8601 import Utc


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

        # create redirects for stdout and stderr
        scenario.stdout = StringIO()
        scenario.stderr = StringIO()
        try:
            test_tags = scenario.tags
        except AttributeError:
            test_tags = ()

        streamresult.status(test_id=get_test_id(scenario),
                            test_status='inprogress',
                            test_tags=test_tags,
                            timestamp=now())


    @before.step_output
    def capture_output(step):

        # only consider steps for background
        if not step.scenario:
            return

        sys.stdout = step.scenario.stdout
        sys.stderr = step.scenario.stderr

    @after.step_output
    def uncapture_output(step):

        sys.stdout = real_stdout
        sys.stderr = real_stderr

    @after.each_scenario
    def after_scenario(scenario):

        streamresult.status(test_id=get_test_id(scenario),
                            file_name='stdout',
                            file_bytes=scenario.stdout.getvalue().encode('utf-8'),
                            mime_type='text/plain; charset=utf8',
                            eof=True)

        streamresult.status(test_id=get_test_id(scenario),
                            file_name='stderr',
                            file_bytes=scenario.stderr.getvalue().encode('utf-8'),
                            mime_type='text/plain; charset=utf8',
                            eof=True)

        if scenario.passed:
            streamresult.status(test_id=get_test_id(scenario),
                                test_status='success',
                                timestamp=now())
        else:
            streamresult.status(test_id=get_test_id(scenario),
                                test_status='fail',
                                timestamp=now())

    @after.each_step
    def after_step(step):

        # only consider steps for background
        if not step.scenario:
            return

        test_id = get_test_id(step.scenario)

        if step.passed:
            marker = u'✔'
        elif not step.defined_at:
            marker = u'?'
        elif step.failed:
            marker = u'❌'

            try:
                streamresult.status(test_id=test_id,
                                    file_name='traceback',
                                    file_bytes=step.why.traceback.encode('utf-8'),
                                    mime_type='text/plain; charset=utf8')
            except AttributeError:
                pass

        elif not step.ran:
            marker = u' '
        else:
            raise AssertionError("Internal error")

        steps = u'{marker} {sentence}\n'.format(
            marker=marker,
            sentence=step.sentence)
        streamresult.status(test_id=test_id,
                        file_name='steps',
                        file_bytes=steps.encode('utf-8'),
                        mime_type='text/plain; charset=utf8')

    @after.all
    def after_all(total):

        streamresult.stopTestRun()
        close_file(file_)


def get_test_id(scenario):
    try:
        return '{feature}: {scenario}'.format(
            feature=scenario.feature.name,
            scenario=scenario.name)
    except AttributeError:
        return '{feature}: Background'.format(
            feature=scenario.feature.name)


def now():
    """
    A timestamp suitable for subunit
    """

    return datetime.datetime.now(tz=Utc())
