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

from lettuce.django.apps import harvest_lettuces

server = None
django_url = None


def get_server(*args, **kwargs):
    """
    Look up the server we are using and set it as the global
    """

    from django.conf import settings

    server_name = getattr(settings, 'LETTUCE_TEST_SERVER',
                          'lettuce.django.server.DefaultServer')
    module, klass = server_name.rsplit('.', 1)

    Server = getattr(__import__(module, fromlist=[klass]), klass)

    global server, django_url

    server = Server(*args, **kwargs)
    django_url = server.url

    return server


__all__ = ['harvest_lettuces', 'server', 'django_url']
