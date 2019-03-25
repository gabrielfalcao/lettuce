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
import traceback
from distutils.version import StrictVersion

import django
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test.utils import setup_test_environment, teardown_test_environment

from lettuce import Runner
from lettuce import registry
from lettuce.core import SummaryTotalResults
from lettuce.exceptions import LettuceRunnerError

from lettuce.django import harvest_lettuces, get_server
from lettuce.django.server import LettuceServerException


DJANGO_VERSION = StrictVersion(django.get_version())


class Command(BaseCommand):
    help = u'Run lettuce tests all along installed apps'

    if DJANGO_VERSION < StrictVersion('1.7'):
        requires_model_validation = False
    else:
        requires_system_checks = False

    def add_arguments(self, parser):
        parser.set_defaults(verbosity=3)  # default verbosity is 3
        parser.add_argument('features', nargs='*', help='A list of features to run (files or folders)')
        parser.add_argument(
            '-a', '--apps', action='store', dest='apps', default='',
            help='Run ONLY the django apps that are listed here. Comma separated'
        )
        parser.add_argument(
            '-A', '--avoid-apps', action='store', dest='avoid_apps', default='',
            help='AVOID running the django apps that are listed here. Comma separated'
        )
        parser.add_argument(
            '-S', '--no-server', action='store_true', dest='no_server', default=False,
            help="will not run django's builtin HTTP server"
        )
        parser.add_argument(
            '--nothreading', action='store_false', dest='use_threading', default=True,
            help='Tells Django to NOT use threading.'
        )
        parser.add_argument(
            '-T', '--test-server', action='store_true', dest='test_database',
            default=getattr(settings, "LETTUCE_USE_TEST_DATABASE", False),
            help="will run django's builtin HTTP server using the test databases"
        )
        parser.add_argument(
            '-P', '--port', type=int, dest='port',
            help="the port in which the HTTP server will run at"
        )
        parser.add_argument(
            '-d', '--debug-mode', action='store_true', dest='debug', default=False,
            help="when put together with builtin HTTP server, forces django to run with settings.DEBUG=True"
        )
        parser.add_argument(
            '-s', '--scenarios', action='store', dest='scenarios', default=None,
            help='Comma separated list of scenarios to run'
        )
        parser.add_argument(
            "-t", "--tag", dest="tags", type=str, action='append', default=None,
            help='Tells lettuce to run the specified tags only; '
                 'can be used multiple times to define more tags'
                 '(prefixing tags with "-" will exclude them and '
                 'prefixing with "~" will match approximate words)'
        )
        parser.add_argument(
            '--with-xunit', action='store_true', dest='enable_xunit', default=False,
            help='Output JUnit XML test results to a file'
        )
        parser.add_argument(
            '--smtp-queue', action='store_true', dest='smtp_queue', default=False,
            help='Use smtp for mail queue (usefull with --no-server option'
        )
        parser.add_argument(
            '--xunit-file', action='store', dest='xunit_file', default=None,
            help='Write JUnit XML to this file. Defaults to lettucetests.xml'
        )
        parser.add_argument(
            '--with-subunit', action='store_true', dest='enable_subunit',
            default=False, help='Output Subunit test results to a file'
        )
        parser.add_argument(
            '--subunit-file', action='store', dest='subunit_file', default=None,
            help='Write Subunit to this file. Defaults to subunit.bin'
        )
        parser.add_argument(
            '--with-jsonreport', action='store_true', dest='enable_jsonreport',
            default=False, help='Output JSON test results to a file'
        )
        parser.add_argument(
            '--jsonreport-file', action='store', dest='jsonreport_file',
            default=None, help='Write JSON report to this file. Defaults to lettucetests.json'
        )
        parser.add_argument(
            "--failfast", dest="failfast", default=False,
            action="store_true", help='Stop running in the first failure'
        )
        parser.add_argument(
            "--pdb", dest="auto_pdb", default=False, action="store_true",
            help='Launches an interactive debugger upon error'
        )
        if DJANGO_VERSION < StrictVersion('1.7'):
            # Django 1.7 introduces the --no-color flag. We must add the flag
            # to be compatible with older django versions
            parser.add_argument(
                '--no-color', action='store_true', dest='no_color',
                default=False, help="Don't colorize the command output."
            )

    def get_paths(self, feature_paths, apps_to_run, apps_to_avoid):
        if feature_paths:
            for path, exists in zip(feature_paths, map(os.path.exists, feature_paths)):
                if not exists:
                    sys.stderr.write("You passed the path '%s', but it does not exist.\n" % path)
                    sys.exit(1)
            else:
                paths = feature_paths
        else:
            paths = harvest_lettuces(apps_to_run, apps_to_avoid)  # list of tuples with (path, app_module)

        return paths

    def handle(self, *args, **options):
        setup_test_environment()

        verbosity = options['verbosity']
        no_color = options.get('no_color', False)
        apps_to_run = tuple(options['apps'].split(","))
        apps_to_avoid = tuple(options['avoid_apps'].split(","))
        run_server = not options['no_server']
        test_database = options['test_database']
        smtp_queue = options['smtp_queue']
        tags = options['tags']
        failfast = options['failfast']
        auto_pdb = options['auto_pdb']
        threading = options['use_threading']

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

            if DJANGO_VERSION < StrictVersion('1.7'):
                call_command('syncdb', verbosity=0, interactive=False,)
                if migrate_south:
                   call_command('migrate', verbosity=0, interactive=False,)
            else:
                call_command('migrate', verbosity=0, interactive=False,)

        settings.DEBUG = options.get('debug', False)

        paths = self.get_paths(options['features'], apps_to_run, apps_to_avoid)
        server = get_server(port=options['port'], threading=threading)

        if run_server:
            try:
                server.start()
            except LettuceServerException as e:
                raise CommandError("Couldn't start Django server: %s" % e)

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
                                enable_jsonreport=options.get('enable_jsonreport'),
                                xunit_filename=options.get('xunit_file'),
                                subunit_filename=options.get('subunit_file'),
                                jsonreport_filename=options.get('jsonreport_file'),
                                tags=tags, failfast=failfast, auto_pdb=auto_pdb,
                                smtp_queue=smtp_queue)

                result = runner.run()
                if app_module is not None:
                    registry.call_hook('after_each', 'app', app_module, result)

                results.append(result)
                if not result or result.steps != result.steps_passed:
                    failed = True
        except LettuceRunnerError:
            failed = True

        except Exception as e:
            failed = True
            traceback.print_exc(e)

        finally:
            summary = SummaryTotalResults(results)
            summary.summarize_all()
            registry.call_hook('after', 'harvest', summary)

            if test_database:
                self._testrunner.teardown_databases(self._old_db_config)

            teardown_test_environment()
            server.stop(failed)

            if failed:
                raise CommandError("Lettuce tests failed.")
