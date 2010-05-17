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
import sys
import urllib
import threading
from StringIO import StringIO
from django.db.models import get_apps
from django.core.management.base import NoArgsCommand
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIServer
from django.core.servers.basehttp import WSGIRequestHandler
from lettuce import Runner
from lettuce import STEP_REGISTRY
from lettuce import CALLBACK_REGISTRY
from lettuce.fs import FileSystem

class Server(threading.Thread):
    """
    Runs django's builtin in background
    """
    address = '0.0.0.0'
    port = 8000

    class RequestHandler(WSGIRequestHandler):
        """ A RequestHandler that silences output, in order to don't
        mess with Lettuce's output"""

        def log_message(self, *args, **kw):
            pass # do nothing

    def run(self):
        server_address = (self.address, self.port)
        httpd = WSGIServer(server_address, self.RequestHandler)
        httpd.set_app(WSGIHandler())
        httpd.serve_forever()

class Command(NoArgsCommand):
    help = u'Run lettuce tests within each django app'

    fs = FileSystem()
    server = Server()

    def _filter_django_apps(self, module):
        "returns only those apps that are not builtin django.contrib"
        return not module.__name__.startswith("django.contrib")

    def iter_app_dirs(self, path="features"):
        apps = filter(self._filter_django_apps, get_apps())
        for app in apps:
            yield self.fs.join(self.fs.dirname(app.__file__), path)

    def wait_for_server(self):
        url = "http://%s:%d" % (self.server.address, self.server.port)
        running = False

        while not running:
            try:
                urllib.urlopen(url)
                running = True
            except IOError:
                pass

    def runserver(self):
        self.server.setDaemon(True)
        self.server.start()
        self.wait_for_server()

    def stopserver(self, failed=False):
        raise SystemExit(int(failed))

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', 4))

        self.runserver()

        failed = False
        try:
            for path in self.iter_app_dirs():
                STEP_REGISTRY.clear()
                CALLBACK_REGISTRY.clear()
                runner = Runner(path, verbosity)
                result = runner.run()
                if result.steps != result.steps_passed:
                    failed = True

        finally:
            self.stopserver(failed)
