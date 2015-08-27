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
import re
import os
import imp
import sys
import codecs
import fnmatch
import zipfile

from functools import wraps
from glob import glob
from os.path import abspath, join, dirname, curdir, exists


class FeatureLoader(object):
    """Loader class responsible for findind features and step
    definitions along a given path on filesystem"""
    def __init__(self, base_dir, root_dir=None):
        self.base_dir = FileSystem.abspath(base_dir)
        if root_dir is None:
            root_dir = '/'
        self.root_dir = FileSystem.abspath(root_dir)

    def find_and_load_step_definitions(self):
        # find steps, possibly up several directories
        base_dir = self.base_dir
        while base_dir != self.root_dir:
            files = FileSystem.locate(base_dir, '*.py')
            if files:
                break
            base_dir = FileSystem.join(base_dir, '..')
        else:
            # went as far as root_dir, also discover files under root_dir
            files = FileSystem.locate(base_dir, '*.py')

        for filename in files:
            root = FileSystem.dirname(filename)
            sys.path.insert(0, root)
            to_load = FileSystem.filename(filename, with_extension=False)
            try:
                module = __import__(to_load)
            except ValueError as e:
                import traceback
                err_msg = traceback.format_exc(e)
                if 'empty module name' in err_msg.lower():
                    continue
                else:
                    e.args = ('{0} when importing {1}'
                              .format(e, filename)),
                    raise e

            reload(module)  # always take fresh meat :)
            sys.path.remove(root)

    def find_feature_files(self):
        paths = FileSystem.locate(self.base_dir, "*.feature")
        paths.sort()
        return paths


class FileSystem(object):
    """File system abstraction, mainly used for indirection, so that
    lettuce can be well unit-tested :)
    """
    stack = []

    def __init__(self):
        self.stack = []

    @classmethod
    def _import(cls, name):
        sys.path.insert(0, cls.current_dir())
        fp, pathname, description = imp.find_module(name)

        try:
            module = imp.load_module(name, fp, pathname, description)
            sys.path.remove(cls.current_dir())
            return module
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

    @classmethod
    def pushd(cls, *path):
        """Change current dir to `path`, adding it to a stack. Can be
        undone by calling FileSystem.popd()"""

        path = cls.join(*path)
        if not len(cls.stack):
            cls.stack.append(cls.current_dir())

        cls.stack.append(path)
        os.chdir(path)

    @classmethod
    def popd(cls):
        """Go back one path in path stack"""
        if cls.stack:
            cls.stack.pop()
            if cls.stack:
                os.chdir(cls.stack[-1])

    @classmethod
    def filename(cls, path, with_extension=True):
        """Returns only the filename from a full path. If the argument
        with_extension is False, return the filename without
        extension.

        Examples::

        >>> from lettuce.fs import FileSystem
        >>> assert FileSystem.filename('/full/path/to/some_file.py') == 'some_file.py'
        >>> assert FileSystem.filename('/full/path/to/some_file.py', False) == 'some_file'

        """
        fname = os.path.split(path)[1]
        if not with_extension:
            fname = os.path.splitext(fname)[0]

        return fname

    @classmethod
    def exists(cls, path):
        """Return True if `path`exists"""
        return exists(path)

    @classmethod
    def mkdir(cls, path):
        """Create paths recursively, ignore already created dirs

        Example:
            >>> from lettuce.fs import FileSystem
            >>> FileSystem.mkdir('~/a/lot/of/nested/dirs')
        """
        try:
            os.makedirs(path)
        except OSError as e:
            # ignore if path already exists
            if e.errno not in (17, ):
                raise e
            else:
                if not os.path.isdir(path):
                    # but the path must be a dir to ignore its creation
                    raise e

    @classmethod
    def current_dir(cls, path=""):
        '''Returns the absolute path for current dir, also join the
        current path with the given, if so.'''
        to_return = cls.abspath(curdir)
        if path:
            return cls.join(to_return, path)

        return to_return

    @classmethod
    def abspath(cls, path):
        '''Returns the absolute path for the given path.'''
        return abspath(path)

    @classmethod
    def relpath(cls, path):
        '''Returns the absolute path for the given path.'''
        current_path = cls.current_dir()
        absolute_path = cls.abspath(path)
        return re.sub("^" + re.escape(current_path), '', absolute_path).lstrip("/")

    @classmethod
    def join(cls, *args):
        '''Returns the concatenated path for the given arguments.'''
        return join(*args)

    @classmethod
    def dirname(cls, path):
        '''Returns the directory name for the given file.'''
        return cls.abspath(dirname(path))

    @classmethod
    def walk(cls, path):
        '''Walks through filesystem'''
        return os.walk(path)

    @classmethod
    def locate(cls, path, match, recursive=True):
        """Locate files recursively in a given path"""
        root_path = cls.abspath(path)
        if recursive:
            return_files = []
            for path, dirs, files in cls.walk(root_path):
                for filename in fnmatch.filter(files, match):
                    return_files.append(cls.join(path, filename))
            return return_files
        else:
            return glob(cls.join(root_path, match))

    @classmethod
    def extract_zip(cls, filename, base_path='.', verbose=False):
        """Extracts a zip file into `base_path`"""
        base_path = cls.abspath(base_path)
        output = lambda x: verbose and sys.stdout.write("%s\n" % x)

        cls.pushd(base_path)
        zfile = zipfile.ZipFile(filename)

        output("Extracting files to %s" % base_path)
        for file_name in zfile.namelist():
            try:
                output("  -> Unpacking %s" % file_name)
                f = cls.open_raw(file_name, 'w')
                f.write(zfile.read(file_name))
                f.close()
            except IOError:
                output("---> Creating directory %s" % file_name)
                cls.mkdir(file_name)

        cls.popd()

    @classmethod
    def open(cls, name, mode):
        """Opens a file as utf-8"""
        path = name
        if not os.path.isabs(path):
            path = cls.current_dir(name)

        return codecs.open(path, mode, 'utf-8')

    @classmethod
    def open_raw(cls, name, mode):
        """Opens a file without specifying encoding"""
        path = name
        if not os.path.isabs(path):
            path = cls.current_dir(name)

        return open(path, mode)

    @classmethod
    def in_directory(cls, *directories):
        """Decorator to set the working directory around a function"""
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                cls.pushd(*directories)

                try:
                    return func(*args, **kwargs)

                finally:
                    cls.popd()
                
            return inner
        return decorator
