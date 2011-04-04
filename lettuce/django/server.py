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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import time
import socket
import httplib
import urlparse
import tempfile
import threading

from StringIO import StringIO

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIServer
from django.core.servers.basehttp import ServerHandler
from django.core.servers.basehttp import WSGIRequestHandler
from django.core.servers.basehttp import WSGIServerException
from django.core.servers.basehttp import AdminMediaHandler

from lettuce.registry import call_hook

class LettuceServerException(WSGIServerException):
    pass

keep_running = True
class StopabbleHandler(object):
    """WSGI middleware that intercepts HTTP method DELETE at / and
    kills through StopIteration exception server"""

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '/' and environ['REQUEST_METHOD'] == 'DELETE':
            global keep_running
            keep_running = False

        return self.application(environ, start_response)

class MutedRequestHandler(WSGIRequestHandler):
    """ A RequestHandler that silences output, in order to don't
    mess with Lettuce's output"""

    dev_null = StringIO()
    def log_message(self, *args, **kw):
        pass # do nothing

    def handle(self):
        """Handle a single HTTP request"""
        self.raw_requestline = self.rfile.readline()
        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = LettuceServerHandler(
            self.rfile,
            self.wfile,
            self.dev_null,
            self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())

class LettuceServerHandler(ServerHandler):
    def finish_response(self):
        try:
            ServerHandler.finish_response(self)

        # avoiding broken pipes
        # http://code.djangoproject.com/ticket/4444
        except Exception:
            exc_type, exc_value = sys.exc_info()[:2]
            if not issubclass(exc_type, socket.error) or exc_value.args[0] is 32:
                raise

class ThreadedServer(threading.Thread):
    """
    Runs django's builtin in background
    """
    lock = threading.Lock()

    def __init__(self, address, port, *args, **kw):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    @staticmethod
    def get_real_address(address):
        if address == '0.0.0.0':
            address = 'localhost'

        return address

    def wait(self):
        address = ThreadedServer.get_real_address(self.address)

        while True:
            time.sleep(0.1)
            http = httplib.HTTPConnection(address, self.port)
            try:
                http.request("GET", "/")
            except socket.error:
                http.close()
                continue
            break

        self.lock.acquire()

    def run(self):
        self.lock.acquire()
        pidfile = os.path.join(tempfile.gettempdir(), 'lettuce-django.pid')
        if os.path.exists(pidfile):
            pid = int(open(pidfile).read())
            try:
                os.kill(pid, 9)

            except OSError:
                pass

            finally:
                os.unlink(pidfile)

        open(pidfile, 'w').write(unicode(os.getpid()))

        bound = False
        max_port = 65535

        connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not bound or self.port < max_port:
            try:
                connector.connect((self.address, self.port))
                self.port += 1

            except socket.error:
                bound = True
                break

        if bound:
            try:
                server_address = (self.address, self.port)
                httpd = WSGIServer(server_address, MutedRequestHandler)
                bound = True
            except WSGIServerException:
                bound = False

        if not bound:
            raise LettuceServerException(
                "the port %d already being used, could not start " \
                "django's builtin server on it" % self.port
            )


        handler = StopabbleHandler(WSGIHandler())
        if 'django.contrib.admin' in settings.INSTALLED_APPS:
            admin_media_path = ''
            handler = AdminMediaHandler(handler, admin_media_path)
            print "Preparing to serve django's admin site static files..."

        httpd.set_app(handler)

        global keep_running
        while keep_running:
            call_hook('before', 'handle_request', httpd, self)
            httpd.handle_request()
            call_hook('after', 'handle_request', httpd, self)
            if self.lock.locked():
                self.lock.release()

class Server(object):
    """A silenced, lightweight and simple django's builtin server so
    that lettuce can be used with selenium, webdriver, windmill or any
    browser tool"""

    def __init__(self, address='0.0.0.0', port=None):
        self.port = int(port or getattr(settings, 'LETTUCE_SERVER_PORT', 8000))
        self.address = unicode(address)
        self._actual_server = ThreadedServer(self.address, self.port)

    def start(self):
        """Starts the webserver thread, and waits it to be available"""
        call_hook('before', 'runserver', self._actual_server)
        self._actual_server.setDaemon(True)
        self._actual_server.start()
        self._actual_server.wait()

        addrport = self.address, self._actual_server.port
        print "Django's builtin server is running at %s:%d" % addrport

    def stop(self, fail=False):
        http = httplib.HTTPConnection(self.address, self.port)
        try:
            http.request("DELETE", "/")
            http.getresponse().read()
        except socket.error:
            pass
        finally:
            http.close()
            code = int(fail)
            call_hook('after', 'runserver', self._actual_server)
            return sys.exit(code)

    def url(self, url=""):
        base_url = "http://%s" % ThreadedServer.get_real_address(self.address)

        if self.port is not 80:
            base_url += ':%d' % self.port

        return urlparse.urljoin(base_url, url)

server = Server()
django_url = server.url
