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
import codecs
import fnmatch
import zipfile

from glob import glob
from os.path import abspath, join, dirname, curdir, exists

class FeatureLoader(object):
    def __init__(self, base_dir):
        self.base_dir = FileSystem.abspath(base_dir)

    def find_and_load_step_definitions(self):
        for root, dirs, files in FileSystem.walk(FileSystem.join(self.base_dir, 'step_definitions')):
            sys.path.insert(0, root)
            for fname in files:
                if fname.endswith(".py"):
                    to_load = FileSystem.filename(fname, with_extension=False)
                    __import__(to_load)
            sys.path.remove(root)
    def find_feature_files(self):
        paths = []
        for root, dirs, files in FileSystem.walk(self.base_dir):
            for filename in files:
                if filename.endswith(".feature"):
                    path = FileSystem.join(root, filename)
                    paths.append(path)

        return paths

class FileSystem(object):
    stack = []

    def __init__(self):
        self.stack = []

    @classmethod
    def pushd(cls, path):
        if not len(cls.stack):
            cls.stack.append(cls.current_dir())

        cls.stack.append(path)
        os.chdir(path)

    @classmethod
    def popd(cls):
        if cls.stack:
            cls.stack.pop()
            if cls.stack:
                os.chdir(cls.stack[-1])

    @classmethod
    def filename(cls, path, with_extension=True):
        fname = os.path.split(path)[1]
        if not with_extension:
            fname = os.path.splitext(fname)[0]

        return fname

    @classmethod
    def exists(cls, path):
        return exists(path)

    @classmethod
    def mkdir(cls, path):
        try:
            os.makedirs(path)
        except OSError, e:
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
    def join(cls, *args):
        '''Returns the concatenated path for the given arguments.'''
        return join(*args)

    @classmethod
    def dirname(cls, path):
        '''Returns the directory name for the given file.'''
        return dirname(path)

    @classmethod
    def walk(cls, path):
        '''Walks through filesystem'''
        return os.walk(path)

    @classmethod
    def locate(cls, path, match, recursive=True):
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
        path = name
        if not os.path.isabs(path):
            path = cls.current_dir(name)

        return codecs.open(path, mode, 'utf-8')

    @classmethod
    def open_raw(cls, name, mode):
        path = name
        if not os.path.isabs(path):
            path = cls.current_dir(name)

        return open(path, mode)

