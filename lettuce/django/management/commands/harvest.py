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
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.test.utils import setup_test_environment
from django.test.utils import teardown_test_environment

from lettuce import Runner
from lettuce import registry

from lettuce.django.server import Server
from lettuce.django import harvest_lettuces
from lettuce.django.server import LettuceServerException


class Command(BaseCommand):
    help = u'Run lettuce tests all along installed apps'
    args = '[PATH to feature file or folder]'
    requires_model_validation = False

    option_list = BaseCommand.option_list[1:] + (
        make_option('-v', '--verbosity', action='store', dest='verbosity', default='4',
            type='choice', choices=map(str, range(5)),
            help='Verbosity level; 0=no output, 1=only dots, 2=only scenario names, 3=colorless output, 4=normal output (colorful)'),

        make_option('-a', '--apps', action='store', dest='apps', default='',
            help='Run ONLY the django apps that are listed here. Comma separated'),

        make_option('-A', '--avoid-apps', action='store', dest='avoid_apps', default='',
            help='AVOID running the django apps that are listed here. Comma separated'),

        make_option('-S', '--no-server', action='store_true', dest='no_server', default=False,
            help="will not run django's builtin HTTP server"),

        make_option('-P', '--port', type='int', dest='port',
            help="the port in which the HTTP server will run at"),

        make_option('-d', '--debug-mode', action='store_true', dest='debug', default=False,
            help="when put together with builtin HTTP server, forces django to run with settings.DEBUG=True"),

        make_option('-s', '--scenarios', action='store', dest='scenarios', default=None,
            help='Comma separated list of scenarios to run'),

        make_option("-t", "--tag",
                    dest="tags",
                    type="str",
                    action='append',
                    default=None,
                    help='Tells lettuce to run the specified tags only; '
                    'can be used multiple times to define more tags'
                    '(prefixing tags with "-" will exclude them and '
                    'prefixing with "~" will match approximate words)'),

        make_option('--with-xunit', action='store_true', dest='enable_xunit', default=False,
            help='Output JUnit XML test results to a file'),

        make_option('--xunit-file', action='store', dest='xunit_file', default=None,
            help='Write JUnit XML to this file. Defaults to lettucetests.xml'),

        make_option("--failfast", dest="failfast", default=False,
                    action="store_true", help='Stop running in the first failure'),

        make_option("--pdb", dest="auto_pdb", default=False,
                    action="store_true", help='Launches an interactive debugger upon error'),
    )

    def stopserver(self, failed=False):
        raise SystemExit(int(failed))

    def get_paths(self, args, apps_to_run, apps_to_avoid):
        if args:
            for path, exists in zip(args, map(os.path.exists, args)):
                if not exists:
                    sys.stderr.write("You passed the path '%s', but it does not exist.\n" % path)
                    sys.exit(1)
            else:
                paths = args
        else:
            paths = harvest_lettuces(apps_to_run, apps_to_avoid)  # list of tuples with (path, app_module)

        return paths

    def handle(self, *args, **options):
        setup_test_environment()

        settings.DEBUG = options.get('debug', False)

        verbosity = int(options.get('verbosity', 4))
        apps_to_run = tuple(options.get('apps', '').split(","))
        apps_to_avoid = tuple(options.get('avoid_apps', '').split(","))
        run_server = not options.get('no_server', False)
        tags = options.get('tags', None)
        failfast = options.get('failfast', False)
        auto_pdb = options.get('auto_pdb', False)

        server = Server(port=options['port'])

        paths = self.get_paths(args, apps_to_run, apps_to_avoid)
        if run_server:
            try:
                server.start()
            except LettuceServerException, e:
                raise SystemExit(e)

        os.environ['SERVER_NAME'] = server.address
        os.environ['SERVER_PORT'] = str(server.port)

        failed = False

        registry.call_hook('before', 'harvest', locals())
        results = []
        try:
            for path in paths:
                app_module = None
                if isinstance(path, tuple) and len(path) is 2:
                    path, app_module = path

                if app_module is not None:
                    registry.call_hook('before_each', 'app', app_module)

                runner = Runner(path, options.get('scenarios'), verbosity,
                                enable_xunit=options.get('enable_xunit'),
                                xunit_filename=options.get('xunit_file'),
                                tags=tags, failfast=failfast, auto_pdb=auto_pdb)

                result = runner.run()
                if app_module is not None:
                    registry.call_hook('after_each', 'app', app_module, result)

                results.append(result)
                if not result or result.steps != result.steps_passed:
                    failed = True
        except SystemExit, e:
            failed = e.code

        except Exception, e:
            failed = True
            import traceback
            traceback.print_exc(e)

        finally:
            registry.call_hook('after', 'harvest', results)
            server.stop(failed)
            teardown_test_environment()
            raise SystemExit(int(failed))
