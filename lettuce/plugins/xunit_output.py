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
# MERsteps.pyCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from datetime import datetime
from lettuce.terrain import after
from lettuce.terrain import before
from xml.dom import minidom


def wrt_output(filename, content):
    f = open(filename, "w")
    f.write(content.encode('utf-8'))
    f.close()

def total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

def enable(filename=None):

    doc = minidom.Document()
    root = doc.createElement("testsuite")
    output_filename = filename or "lettucetests.xml"

    @before.each_step
    def time_step(step):
        step.started = datetime.now()

    @after.each_step
    def create_test_case(step):
        classname = "%s : %s" % (step.scenario.feature.name, step.scenario.name)
        tc = doc.createElement("testcase")
        tc.setAttribute("classname", classname)
        tc.setAttribute("name", step.sentence)
        tc.setAttribute("time", str(total_seconds((datetime.now() - step.started))))

        if step.failed:
            cdata = doc.createCDATASection(step.why.traceback)
            failure = doc.createElement("failure")
            failure.setAttribute("message",step.why.cause)
            failure.appendChild(cdata)
            tc.appendChild(failure)

        root.appendChild(tc)

    @after.all
    def output_xml(total):
        root.setAttribute("tests", str(total.steps))
        root.setAttribute("failed", str(total.steps_failed))
        doc.appendChild(root)
        wrt_output(output_filename, doc.toxml())

