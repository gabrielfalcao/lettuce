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

from os.path import join, dirname
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
from django.conf import settings


def _filter_bultins(module):
    "returns only those apps that are not builtin django.contrib"
    name = module.__name__
    return not name.startswith("django.contrib") and name != 'lettuce.django'


def _filter_configured_apps(module):
    "returns only those apps that are in django.conf.settings.LETTUCE_APPS"
    app_found = True
    if hasattr(settings, 'LETTUCE_APPS') and isinstance(settings.LETTUCE_APPS, tuple):
        app_found = False
        for appname in settings.LETTUCE_APPS:
            if module.__name__.startswith(appname):
                app_found = True

    return app_found


def _filter_configured_avoids(module):
    "returns apps that are not within django.conf.settings.LETTUCE_AVOID_APPS"
    run_app = False
    if hasattr(settings, 'LETTUCE_AVOID_APPS') and isinstance(settings.LETTUCE_AVOID_APPS, tuple):
        for appname in settings.LETTUCE_AVOID_APPS:
            if module.__name__.startswith(appname):
                run_app = True

    return not run_app


def get_apps():
    return map(import_module, settings.INSTALLED_APPS)


def harvest_lettuces(only_the_apps=None, avoid_apps=None, path="features"):
    """gets all installed apps that are not from django.contrib
    returns a list of tuples with (path_to_app, app_module)
    """

    apps = get_apps()

    if isinstance(only_the_apps, tuple) and any(only_the_apps):

        def _filter_only_specified(module):
            return module.__name__ in only_the_apps
        apps = filter(_filter_only_specified, apps)
    else:
        apps = filter(_filter_bultins, apps)
        apps = filter(_filter_configured_apps, apps)
        apps = filter(_filter_configured_avoids, apps)

    if isinstance(avoid_apps, tuple) and any(avoid_apps):

        def _filter_avoid(module):
            return module.__name__ not in avoid_apps

        apps = filter(_filter_avoid, apps)

    joinpath = lambda app: (join(dirname(app.__file__), path), app)
    return map(joinpath, apps)
