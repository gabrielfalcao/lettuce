#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from os.path import abspath, dirname, join, split, curdir
from nose.tools import assert_equals
from lettuce.fs import FileSystem

def test_abspath():
    fs = FileSystem()
    p = fs.abspath(".")
    p2 = abspath(".")

    assert p == p2

def test_relpath():
    fs = FileSystem()
    p = fs.relpath(join(curdir, 'other'))
    p2 = join(dirname(curdir), 'other')

    assert_equals(p, p2)

def test_current_dir_with_join():
    fs = FileSystem()
    got = fs.current_dir("etc")
    expected = join(abspath("."), "etc")

    assert_equals(got, expected)

def test_current_dir_without_join():
    fs = FileSystem()
    got = fs.current_dir()
    expected = abspath(".")

    assert_equals(got, expected)

def test_join():
    fs = FileSystem()
    p = fs.join(fs.abspath("."), "test")
    p2 = join(abspath("."), "test")

    assert p == p2, "Expected:\n%r\nGot:\n%r" % (p2, p)

def test_dirname():
    fs = FileSystem()
    p = fs.dirname(fs.abspath("."))
    p2 = dirname(abspath("."))

    assert p == p2, "Expected:\n%r\nGot:\n%r" % (p2, p)

def test_recursive_locate():
    fs = FileSystem()
    files = fs.locate(path=abspath(join(dirname(__file__), "files_to_locate")), match="*.txt", recursive=True)

    assert files
    assert isinstance(files, list)
    assert len(files) == 2
    assert split(files[0])[-1] == "test.txt"
    assert split(files[1])[-1] == "test2.txt"
    assert split(split(files[1])[0])[-1] == "sub"

def test_non_recursive_locate():
    fs = FileSystem()
    files = fs.locate(path=abspath(join(dirname(__file__), "files_to_locate")), match="*.txt", recursive=False)

    assert files
    assert isinstance(files, list)
    assert len(files) == 1
    assert split(files[0])[-1] == "test.txt"

def test_open_non_abspath():
    fs = FileSystem()
    assert fs.open('tests/functional/data/some.txt', 'r').read() == 'some text here!\n'

def test_open_abspath():
    fs = FileSystem()
    assert fs.open(abspath('./tests/functional/data/some.txt'), 'r').read() == 'some text here!\n'

def test_open_raw_non_abspath():
    fs = FileSystem()
    assert fs.open_raw('tests/functional/data/some.txt', 'r').read() == 'some text here!\n'

def test_open_raw_abspath():
    fs = FileSystem()
    assert fs.open_raw(abspath('./tests/functional/data/some.txt'), 'r').read() == 'some text here!\n'
