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
import time
import socket
import httplib
import urlparse
import tempfile
import multiprocessing

from StringIO import StringIO

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIServer
from django.core.servers.basehttp import ServerHandler
from django.core.servers.basehttp import WSGIRequestHandler

try:
    from django.core.servers.basehttp import AdminMediaHandler
except ImportError:
    AdminMediaHandler = None
    
if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    try:
        from django.contrib.staticfiles.handlers import StaticFilesHandler
    except ImportError:
        StaticFilesHandler = None
else:
    StaticFilesHandler = None
    
try:
    from django.utils.six.moves import socketserver
except ImportError:
    import SocketServer as socketserver

try:
    import SocketServer
    SocketServer.BaseServer.handle_error = lambda *args, **kw: None
except ImportError:
    pass

from lettuce.django import mail
from lettuce.registry import call_hook


def create_mail_queue():
    mail.queue = multiprocessing.Queue()
    return mail.queue


class LettuceServerException(socket.error):
    pass

keep_running = True


class MutedRequestHandler(WSGIRequestHandler):
    """ A RequestHandler that silences output, in order to don't
    mess with Lettuce's output"""

    dev_null = StringIO()

    def log_message(self, *args, **kw):
        pass  # do nothing

    def handle(self):
        """Handle a single HTTP request"""
        self.raw_requestline = self.rfile.readline()
        if not self.parse_request():  # An error code has been sent, just exit
            return

        handler = LettuceServerHandler(
            self.rfile,
            self.wfile,
            self.dev_null,
            self.get_environ(),
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())


class LettuceServerHandler(ServerHandler):
    def handle_error(self, request, client_address):
        pass

    def finish_response(self):
        try:
            ServerHandler.finish_response(self)

        # avoiding broken pipes
        # http://code.djangoproject.com/ticket/4444
        except Exception:
            exc_type, exc_value = sys.exc_info()[:2]
            if not issubclass(exc_type, socket.error) or \
                   exc_value.args[0] is 32:
                raise


class ThreadedServer(multiprocessing.Process):
    """
    Runs django's builtin in background
    """
    daemon = True

    def __init__(self, address, port, mail_queue, threading=True, *args, **kw):
        multiprocessing.Process.__init__(self)
        self.address = address
        self.port = port
        self.lock = multiprocessing.Lock()
        self.mail_queue = mail_queue
        self.threading = threading
        
    def configure_mail_queue(self):
        mail.queue = self.mail_queue
        settings.EMAIL_BACKEND = \
            'lettuce.django.mail.backends.QueueEmailBackend'

    @staticmethod
    def get_real_address(address):
        if address == '0.0.0.0' or address == 'localhost':
            address = '127.0.0.1'

        return address

    def wait(self):
        address = ThreadedServer.get_real_address(self.address)

        while True:
            time.sleep(0.1)
            http = httplib.HTTPConnection(address, self.port, timeout=1)
            try:
                http.request("GET", "/")
            except socket.error:
                http.close()
                continue
            break

        self.lock.acquire()

    def should_serve_static_files(self):
        try:
            return (StaticFilesHandler is not None and
                    getattr(settings, 'STATIC_URL', False))
        except ImportError:
            return False

    def should_serve_admin_media(self):
        try:
            return (('django.contrib.admin' in settings.INSTALLED_APPS and
                     AdminMediaHandler) or
                    getattr(settings, 'LETTUCE_SERVE_ADMIN_MEDIA', False))
        except ImportError:
            return False

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

        self.configure_mail_queue()

        connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.threading:
            httpd_cls = type(str('WSGIServer'), (socketserver.ThreadingMixIn, WSGIServer), {})
        else:
            httpd_cls = WSGIServer

        try:
            s = connector.connect((self.address, self.port))
            self.lock.release()
            os.kill(os.getpid(), 9)
        except socket.error:
            pass

        finally:
            self.lock.release()

        try:
            server_address = (self.address, self.port)
            httpd = httpd_cls(server_address, MutedRequestHandler)

        except socket.error:
            raise LettuceServerException(
                "the port %d already being used, could not start " \
                "django's builtin server on it" % self.port,
            )

        handler = WSGIHandler()
        if self.should_serve_admin_media():
            if not AdminMediaHandler:
                raise LettuceServerException(
                    "AdminMediaHandler is not available in this version of "
                    "Django. Please set LETTUCE_SERVE_ADMIN_MEDIA = False "
                    "in your Django settings.")
            admin_media_path = ''
            handler = AdminMediaHandler(handler, admin_media_path)

        if self.should_serve_static_files():
            handler = StaticFilesHandler(handler)

        httpd.set_app(handler)

        global keep_running
        while keep_running:
            call_hook('before', 'handle_request', httpd, self)
            httpd.handle_request()
            call_hook('after', 'handle_request', httpd, self)
            try:
                self.lock.release()
            except ValueError:
                pass


class BaseServer(object):
    """
    Base class for Lettuce's internal server
    """

    def __init__(self, address='0.0.0.0', port=None, threading=True):
        self.port = int(port or getattr(settings, 'LETTUCE_SERVER_PORT', 8000))
        self.address = unicode(address)
        self.threading = threading

    def start(self):
        """
        Starts the webserver and waits it to be available

        Chain this method up before your implementation
        """
        call_hook('before', 'runserver', self._server)

    def stop(self):
        """
        Stops the webserver

        Chain this method up after your implementation
        """

        call_hook('after', 'runserver', self._server)

    def url(self, url=''):
        """The url to access a server on"""
        raise NotImplemented()


class DefaultServer(BaseServer):
    """A silenced, lightweight and simple django's builtin server so
    that lettuce can be used with selenium, webdriver, windmill or any
    browser tool"""

    def __init__(self, *args, **kwargs):
        super(DefaultServer, self).__init__(*args, **kwargs)

        queue = create_mail_queue()
        self._server = ThreadedServer(self.address, self.port, queue, threading=self.threading)


    def start(self):
        super(DefaultServer, self).start()

        if self._server.should_serve_admin_media():
            msg = "Preparing to serve django's admin site static files"
            if getattr(settings, 'LETTUCE_SERVE_ADMIN_MEDIA', False):
                msg += ' (as per settings.LETTUCE_SERVE_ADMIN_MEDIA=True)'

            print "%s..." % msg

        self._server.start()
        self._server.wait()

        addrport = self.address, self._server.port
        if not self._server.is_alive():
            raise LettuceServerException(
                'Lettuce could not run the builtin Django server at %s:%d"\n'
                'maybe you forgot a "runserver" instance running ?\n\n'
                'well if you really do not want lettuce to run the server '
                'for you, then just run:\n\n'
                'python manage.py --no-server' % addrport,
            )

        print "Django's builtin server is running at %s:%d" % addrport

    def stop(self, fail=False):
        pid = self._server.pid
        if pid:
            os.kill(pid, 9)

        super(DefaultServer, self).stop()

        code = int(fail)
        return sys.exit(code)

    def url(self, url=""):
        base_url = "http://%s" % ThreadedServer.get_real_address(self.address)

        if self.port is not 80:
            base_url += ':%d' % self.port

        return urlparse.urljoin(base_url, url)


try:
    try:
        from django.contrib.staticfiles.testing import \
            StaticLiveServerTestCase as LiveServerTestCase
    except ImportError:
        from django.test.testcases import LiveServerTestCase

    class DjangoServer(BaseServer):
        """
        A server that uses Django's LiveServerTestCase to implement the Server class.
        """

        _server = None

        def start(self):
            super(DjangoServer, self).start()

            os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = \
                    '{address}:{port}'.format(address=self.address,
                                              port=self.port)
            LiveServerTestCase.setUpClass()

            print "Django's builtin server is running at {address}:{port}".format(
                address=self.address,
                port=self.port)

        def stop(self, fail=False):
            LiveServerTestCase.tearDownClass()

            super(DjangoServer, self).stop()

            return 0

        def url(self, url=''):
            return urlparse.urljoin(
                'http://{address}:{port}/'.format(address=self.address,
                                                  port=self.port),
                url)

except ImportError:
    pass
