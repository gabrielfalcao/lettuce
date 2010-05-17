# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.test.utils import setup_test_environment
from django.test.utils import teardown_test_environment

from lettuce import Runner
from lettuce import registry

from lettuce.django import Server
from lettuce.django import harvest_lettuces

class Command(NoArgsCommand):
    help = u'Run lettuce tests within each django app'
    server = Server()

    def stopserver(self, failed=False):
        raise SystemExit(int(failed))

    def handle_noargs(self, **options):
        settings.DEBUG = False
        setup_test_environment()

        verbosity = int(options.get('verbosity', 4))

        self.server.start()

        failed = False
        try:
            for path in harvest_lettuces():
                registry.clear()
                result = Runner(path, verbosity).run()

                if result.steps != result.steps_passed:
                    failed = True

        finally:
            self.server.stop(failed)
            teardown_test_environment()
