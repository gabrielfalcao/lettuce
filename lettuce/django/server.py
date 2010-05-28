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
import os
import sys
import httplib
import urlparse
import tempfile
import threading

from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIServer
from django.core.servers.basehttp import WSGIRequestHandler
from django.core.servers.basehttp import WSGIServerException

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

    def log_message(self, *args, **kw):
        pass # do nothing


class ThreadedServer(threading.Thread):
    """
    Runs django's builtin in background
    """
    lock = threading.Lock()

    def __init__(self, address, port, *args, **kw):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

    def wait(self):
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
        while not bound or self.port > max_port:
            try:
                server_address = (self.address, self.port)
                httpd = WSGIServer(server_address, MutedRequestHandler)
                bound = True
            except WSGIServerException:
                self.port += 1

        if not bound:
            raise LettuceServerException(
                "the port %d already being used, could not start " \
                "django's builtin server on it" % self.port
            )

        httpd.set_app(StopabbleHandler(WSGIHandler()))
        self.lock.release()

        global keep_running
        while keep_running:
            httpd.handle_request()

class Server(object):
    """A silenced, lightweight and simple django's builtin server so
    that lettuce can be used with selenium, webdriver, windmill or any
    browser tool"""

    def __init__(self, address='0.0.0.0', port=8000):
        self.address = unicode(address)
        self.port = int(port)
        self._actual_server = ThreadedServer(self.address, self.port)

    def start(self):
        """Starts the webserver thread, and waits it to be available"""
        self._actual_server.setDaemon(True)
        self._actual_server.start()
        self._actual_server.wait()

        print "Django's builtin server is running at %s:%d" % (self.address, self.port)

    def stop(self, fail=False):
        http = httplib.HTTPConnection(self.address, self.port)
        http.request("DELETE", "/")
        http.getresponse().read()
        http.close()
        code = int(fail)
        return sys.exit(code)

    def url(self, url):
        return urlparse.urljoin("http://%s:%d" % (self.address, self.port), url)

server = Server()
django_url = server.url
