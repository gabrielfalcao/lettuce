#!/usr/bin/env python
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
import os
import sys
import optparse

import lettuce


def main(args=sys.argv[1:]):
    base_path = os.path.join(os.path.dirname(os.curdir), 'features')
    parser = optparse.OptionParser(
        usage="%prog or type %prog -h (--help) for help",
        version=lettuce.version)

    parser.add_option("-v", "--verbosity",
                      dest="verbosity",
                      default=3,
                      help='The verbosity level')

    parser.add_option("--no-color",
                      action="store_true",
                      dest="no_color",
                      default=False,
                      help="Don't colorize the command output.")

    parser.add_option("-s", "--scenarios",
                      dest="scenarios",
                      default=None,
                      help='Comma separated list of scenarios to run')

    parser.add_option("-t", "--tag",
                      dest="tags",
                      default=None,
                      action='append',
                      help='Tells lettuce to run the specified tags only; '
                      'can be used multiple times to define more tags'
                      '(prefixing tags with "-" will exclude them and '
                      'prefixing with "~" will match approximate words)')

    parser.add_option("-r", "--random",
                      dest="random",
                      action="store_true",
                      default=False,
                      help="Run scenarios in a more random order to avoid interference")

    parser.add_option("--root-dir",
                      dest="root_dir",
                      default="/",
                      type="string",
                      help="Tells lettuce not to search for features/steps "
                      " above this directory.")

    parser.add_option("--with-xunit",
                      dest="enable_xunit",
                      action="store_true",
                      default=False,
                      help='Output JUnit XML test results to a file')

    parser.add_option("--xunit-file",
                      dest="xunit_file",
                      default=None,
                      type="string",
                      help='Write JUnit XML to this file. Defaults to '
                      'lettucetests.xml')

    parser.add_option("--with-subunit",
                      dest="enable_subunit",
                      action="store_true",
                      default=False,
                      help='Output Subunit test results to a file')

    parser.add_option("--subunit-file",
                      dest="subunit_filename",
                      default=None,
                      help='Write Subunit data to this file. Defaults to '
                      'subunit.bin')

    parser.add_option("--failfast",
                      dest="failfast",
                      default=False,
                      action="store_true",
                      help='Stop running in the first failure')

    parser.add_option("--pdb",
                      dest="auto_pdb",
                      default=False,
                      action="store_true",
                      help='Launches an interactive debugger upon error')

    options, args = parser.parse_args(args)
    if args:
        base_path = os.path.abspath(args[0])

    try:
        options.verbosity = int(options.verbosity)
    except ValueError:
        pass

    tags = None
    if options.tags:
        tags = [tag.strip('@') for tag in options.tags]

    runner = lettuce.Runner(
        base_path,
        scenarios=options.scenarios,
        verbosity=options.verbosity,
        random=options.random,
        enable_xunit=options.enable_xunit,
        xunit_filename=options.xunit_file,
        enable_subunit=options.enable_subunit,
        subunit_filename=options.subunit_filename,
        failfast=options.failfast,
        auto_pdb=options.auto_pdb,
        tags=tags,
        root_dir=options.root_dir,
    )

    result = runner.run()
    failed = result is None or result.steps != result.steps_passed
    raise SystemExit(int(failed))

if __name__ == '__main__':
    main()
