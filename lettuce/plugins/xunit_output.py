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

from datetime import datetime, timedelta
from lettuce.terrain import after
from lettuce.terrain import before
from xml.dom import minidom
from lettuce.strings import utf8_string


def wrt_output(filename, content):
    f = open(filename, "w")
    if isinstance(content, unicode):
        content = content.encode('utf-8')

    f.write(content)
    f.close()


def write_xml_doc(filename, doc):
    wrt_output(filename, doc.toxml())


def total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


def enable(filename=None):

    doc = minidom.Document()
    root = doc.createElement("testsuite")
    root.setAttribute("name", "lettuce")
    root.setAttribute("hostname", "localhost")
    root.setAttribute("timestamp", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    output_filename = filename or "lettucetests.xml"

    @before.each_step
    def time_step(step):
        step.started = datetime.now()

    @after.each_step
    def create_test_case_step(step):
        parent = step.scenario or step.background
        if getattr(parent, 'outlines', None):
            return
        
        name = getattr(parent, 'name', 'Background')    # Background sections are nameless
        classname = u"%s : %s" % (parent.feature.name, name)
        tc = doc.createElement("testcase")
        tc.setAttribute("classname", classname)
        tc.setAttribute("name", step.sentence)
        try:
            tc.setAttribute("time", str(total_seconds((datetime.now() - step.started))))
        except AttributeError:
            tc.setAttribute("time", str(total_seconds(timedelta(seconds=0))))

        if not step.ran:
            skip = doc.createElement("skipped")
            skip.setAttribute("type", "UndefinedStep(%s)" % step.sentence)
            tc.appendChild(skip)

        if step.failed:
            cdata = doc.createCDATASection(step.why.traceback)
            failure = doc.createElement("failure")
            if hasattr(step.why, 'cause'):
                failure.setAttribute("message", step.why.cause)
            failure.setAttribute("type", step.why.exception.__class__.__name__)
            failure.appendChild(cdata)
            tc.appendChild(failure)

        root.appendChild(tc)

    @before.outline
    def time_outline(scenario, order, outline, reasons_to_fail):
        scenario.outline_started = datetime.now()
        pass

    @after.outline
    def create_test_case_outline(scenario, order, outline, reasons_to_fail):
        classname = "%s : %s" % (scenario.feature.name, scenario.name)
        tc = doc.createElement("testcase")
        tc.setAttribute("classname", classname)
        tc.setAttribute("name", u'| %s |' % u' | '.join(outline.values()))
        tc.setAttribute("time", str(total_seconds((datetime.now() - scenario.outline_started))))

        for reason_to_fail in reasons_to_fail:
            cdata = doc.createCDATASection(reason_to_fail.traceback)
            failure = doc.createElement("failure")
            failure.setAttribute("message", reason_to_fail.cause if hasattr(reason_to_fail,"cause") else "")
            failure.appendChild(cdata)
            tc.appendChild(failure)

        root.appendChild(tc)

    @after.all
    def output_xml(total):
        root.setAttribute("tests", str(total.steps))
        root.setAttribute("failures", str(total.steps_failed))
        root.setAttribute("errors", '0')
        root.setAttribute("time", '0')
        doc.appendChild(root)
        write_xml_doc(output_filename, doc)
