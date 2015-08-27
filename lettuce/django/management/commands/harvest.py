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
import django
from distutils.version import StrictVersion
from optparse import make_option
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.test.utils import setup_test_environment
from django.test.utils import teardown_test_environment

from lettuce import Runner
from lettuce import registry
from lettuce.core import SummaryTotalResults

from lettuce.django import harvest_lettuces, get_server
from lettuce.django.server import LettuceServerException


class Command(BaseCommand):
    help = u'Run lettuce tests all along installed apps'
    args = '[PATH to feature file or folder]'
    requires_model_validation = False

    option_list = BaseCommand.option_list + (
        make_option('-a', '--apps', action='store', dest='apps', default='',
            help='Run ONLY the django apps that are listed here. Comma separated'),

        make_option('-A', '--avoid-apps', action='store', dest='avoid_apps', default='',
            help='AVOID running the django apps that are listed here. Comma separated'),

        make_option('-S', '--no-server', action='store_true', dest='no_server', default=False,
            help="will not run django's builtin HTTP server"),

        make_option('--nothreading', action='store_false', dest='use_threading', default=True,
            help='Tells Django to NOT use threading.'),

        make_option('-T', '--test-server', action='store_true', dest='test_database',
            default=getattr(settings, "LETTUCE_USE_TEST_DATABASE", False),
            help="will run django's builtin HTTP server using the test databases"),

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

        make_option('--smtp-queue', action='store_true', dest='smtp_queue', default=False,
                    help='Use smtp for mail queue (usefull with --no-server option'),

        make_option('--xunit-file', action='store', dest='xunit_file', default=None,
            help='Write JUnit XML to this file. Defaults to lettucetests.xml'),

        make_option('--with-subunit',
                    action='store_true',
                    dest='enable_subunit',
                    default=False,
                    help='Output Subunit test results to a file'),

        make_option('--subunit-file',
                    action='store',
                    dest='subunit_file',
                    default=None,
                    help='Write Subunit to this file. Defaults to subunit.bin'),

        make_option("--failfast", dest="failfast", default=False,
                    action="store_true", help='Stop running in the first failure'),

        make_option("--pdb", dest="auto_pdb", default=False,
                    action="store_true", help='Launches an interactive debugger upon error'),

    )

    def create_parser(self, prog_name, subcommand):
        parser = super(Command, self).create_parser(prog_name, subcommand)
        parser.remove_option('-v')
        help_text = ('Verbosity level; 0=no output, 1=only dots, 2=only '
                     'scenario names, 3=normal output, 4=normal output '
                     '(colorful, deprecated)')
        parser.add_option('-v', '--verbosity',
                          action='store',
                          dest='verbosity',
                          default='3',
                          type='choice',
                          choices=map(str, range(5)),
                          help=help_text)
        if StrictVersion(django.get_version()) < StrictVersion('1.7'):
            # Django 1.7 introduces the --no-color flag. We must add the flag
            # to be compatible with older django versions
            parser.add_option('--no-color',
                              action='store_true',
                              dest='no_color',
                              default=False,
                              help="Don't colorize the command output.")
        return parser

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

        verbosity = int(options.get('verbosity', 3))
        no_color = int(options.get('no_color', False))
        apps_to_run = tuple(options.get('apps', '').split(","))
        apps_to_avoid = tuple(options.get('avoid_apps', '').split(","))
        run_server = not options.get('no_server', False)
        test_database = options.get('test_database', False)
        smtp_queue = options.get('smtp_queue', False)
        tags = options.get('tags', None)
        failfast = options.get('failfast', False)
        auto_pdb = options.get('auto_pdb', False)
        threading = options.get('use_threading', True)
        with_summary = options.get('summary_display', False)

        if test_database:
            migrate_south = getattr(settings, "SOUTH_TESTS_MIGRATE", True)
            try:
                from south.management.commands import patch_for_test_db_setup
                patch_for_test_db_setup()
            except:
                migrate_south = False
                pass

            from django.test.utils import get_runner
            self._testrunner = get_runner(settings)(interactive=False)
            self._testrunner.setup_test_environment()
            self._old_db_config = self._testrunner.setup_databases()

            call_command('syncdb', verbosity=0, interactive=False,)
            if migrate_south:
               call_command('migrate', verbosity=0, interactive=False,)

        settings.DEBUG = options.get('debug', False)

        paths = self.get_paths(args, apps_to_run, apps_to_avoid)
        server = get_server(port=options['port'], threading=threading)

        if run_server:
            try:
                server.start()
            except LettuceServerException as e:
                raise SystemExit(e)

        os.environ['SERVER_NAME'] = str(server.address)
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

                runner = Runner(path, options.get('scenarios'),
                                verbosity, no_color,
                                enable_xunit=options.get('enable_xunit'),
                                enable_subunit=options.get('enable_subunit'),
                                xunit_filename=options.get('xunit_file'),
                                subunit_filename=options.get('subunit_file'),
                                tags=tags, failfast=failfast, auto_pdb=auto_pdb,
                                smtp_queue=smtp_queue)

                result = runner.run()
                if app_module is not None:
                    registry.call_hook('after_each', 'app', app_module, result)

                results.append(result)
                if not result or result.steps != result.steps_passed:
                    failed = True
        except SystemExit as e:
            failed = e.code

        except Exception as e:
            failed = True
            import traceback
            traceback.print_exc(e)

        finally:
            summary = SummaryTotalResults(results)
            summary.summarize_all()
            registry.call_hook('after', 'harvest', summary)

            if test_database:
                self._testrunner.teardown_databases(self._old_db_config)

            teardown_test_environment()
            server.stop(failed)

            raise SystemExit(int(failed))
