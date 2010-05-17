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

from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIServer
from django.core.servers.basehttp import WSGIRequestHandler

class ThreadedServer(threading.Thread):
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


def wait_for_server(address, port):
    url = "http://%s:%d" % (address, port)
    running = False

    while not running:
        try:
            urllib.urlopen(url)
            running = True
        except IOError:
            pass

class Server(object):
    """A silenced, lightweight and simple django's builtin server so
    that lettuce can be used with selenium, webdriver, windmill or any
    browser tool"""

    def __init__(self, address='0.0.0.0', port=8000):
        self.address = unicode(address)
        self.port = int(port)
        self._actual_server = ThreadedServer()

    def start(self):
        """Starts the webserver thread, and waits it to be available"""
        self._actual_server.setDaemon(True)
        self._actual_server.start()
        wait_for_server(self.address, self.port)

    def stop(self, fail=False):
        code = int(fail)
        return sys.exit(code)





