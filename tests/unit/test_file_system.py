# -*- coding: utf-8 -*-
import sys
from StringIO import StringIO
from mox import Mox
from nose.tools import assert_equals
from nose.tools import assert_raises
from lettuce import fs as io

def test_has_a_stack_list():
    "FileSystem stack list"
    assert hasattr(io.FileSystem, 'stack'), \
           'FileSystem should have a stack'
    assert isinstance(io.FileSystem.stack, list), \
           'FileSystem.stack should be a list'

def test_instance_stack_is_not_the_same_as_class_level():
    "FileSystem stack list has different lifecycle in FileSystem objects"
    class MyFs(io.FileSystem):
        pass

    MyFs.stack.append('foo')
    MyFs.stack.append('bar')
    assert_equals(MyFs().stack, [])

def test_pushd_appends_current_dir_to_stack_if_empty():
    "Default behaviour of pushd() is adding the current dir to the stack"
    mox = Mox()
    old_os = io.os
    io.os = mox.CreateMockAnything()

    class MyFs(io.FileSystem):
        stack = []

        @classmethod
        def current_dir(cls):
            return 'should be current dir'

    io.os.chdir('somewhere')

    mox.ReplayAll()
    try:
        assert len(MyFs.stack) is 0
        MyFs.pushd('somewhere')
        assert len(MyFs.stack) is 2
        assert_equals(MyFs.stack, ['should be current dir',
                                   'somewhere'])
        mox.VerifyAll()
    finally:
        io.os = old_os

def test_pushd():
    "FileSystem.pushd"
    mox = Mox()
    old_os = io.os
    io.os = mox.CreateMockAnything()

    class MyFs(io.FileSystem):
        stack = ['first']

    io.os.chdir('second')

    mox.ReplayAll()
    try:
        assert len(MyFs.stack) is 1
        MyFs.pushd('second')
        assert len(MyFs.stack) is 2
        assert_equals(MyFs.stack, ['first',
                                   'second'])
        mox.VerifyAll()
    finally:
        io.os = old_os

def test_pop_with_more_than_1_item():
    "FileSystem.popd with more than 1 item"
    mox = Mox()
    old_os = io.os
    io.os = mox.CreateMockAnything()

    class MyFs(io.FileSystem):
        stack = ['one', 'two']

    io.os.chdir('one')

    mox.ReplayAll()
    try:
        assert len(MyFs.stack) is 2
        MyFs.popd()
        assert len(MyFs.stack) is 1
        assert_equals(MyFs.stack, ['one'])
        mox.VerifyAll()
    finally:
        io.os = old_os

def test_pop_with_1_item():
    "FileSystem.pop behaviour with only one item"
    mox = Mox()
    old_os = io.os
    io.os = mox.CreateMockAnything()

    class MyFs(io.FileSystem):
        stack = ['one']

    mox.ReplayAll()
    try:
        assert len(MyFs.stack) is 1
        MyFs.popd()
        assert len(MyFs.stack) is 0
        assert_equals(MyFs.stack, [])
        mox.VerifyAll()
    finally:
        io.os = old_os

def test_pop_with_no_item():
    "FileSystem.pop behaviour without items in stack"
    mox = Mox()
    old_os = io.os
    io.os = mox.CreateMockAnything()

    class MyFs(io.FileSystem):
        stack = []

    mox.ReplayAll()
    try:
        assert len(MyFs.stack) is 0
        MyFs.popd()
        assert len(MyFs.stack) is 0
        assert_equals(MyFs.stack, [])
        mox.VerifyAll()
    finally:
        io.os = old_os

def test_filename_with_extension():
    "FileSystem.filename with extension"
    got = io.FileSystem.filename('/path/to/filename.jpg')
    assert_equals(got, 'filename.jpg')

def test_filename_without_extension():
    "FileSystem.filename without extension"
    got = io.FileSystem.filename('/path/to/filename.jpg', False)
    assert_equals(got, 'filename')

def test_dirname():
    "FileSystem.dirname"
    got = io.FileSystem.dirname('/path/to/filename.jpg')
    assert_equals(got, '/path/to')

def test_exists():
    "FileSystem.exists"
    mox = Mox()
    old_exists = io.exists
    io.exists = mox.CreateMockAnything()

    io.exists('some path').AndReturn('should be bool')

    mox.ReplayAll()
    try:
        got = io.FileSystem.exists('some path')
        assert_equals(got, 'should be bool')
        mox.VerifyAll()
    finally:
        io.exists = old_exists

def test_extract_zip_non_verbose():
    "FileSystem.extract_zip non-verbose"
    mox = Mox()
    class MyFs(io.FileSystem):
        stack = []
        abspath = mox.CreateMockAnything()
        pushd = mox.CreateMockAnything()
        popd = mox.CreateMockAnything()
        open_raw = mox.CreateMockAnything()
        mkdir = mox.CreateMockAnything()

    mox.StubOutWithMock(io, 'zipfile')

    filename = 'modafoca.zip'
    base_path = '../to/project'
    full_path = '/full/path/to/project'

    MyFs.abspath(base_path).AndReturn(full_path)
    MyFs.pushd(full_path)

    zip_mock = mox.CreateMockAnything()

    io.zipfile.ZipFile(filename).AndReturn(zip_mock)

    file_list = [
        'settings.yml',
        'app',
        'app/controllers.py'
    ]
    zip_mock.namelist().AndReturn(file_list)
    zip_mock.read('settings.yml').AndReturn('settings.yml content')
    zip_mock.read('app/controllers.py').AndReturn('controllers.py content')

    file_mock1 = mox.CreateMockAnything()
    MyFs.open_raw('settings.yml', 'w').AndReturn(file_mock1)
    file_mock1.write('settings.yml content')
    file_mock1.close()

    MyFs.open_raw('app', 'w').AndRaise(IOError('it is a directory, dumb ass!'))
    MyFs.mkdir('app')

    file_mock2 = mox.CreateMockAnything()
    MyFs.open_raw('app/controllers.py', 'w').AndReturn(file_mock2)
    file_mock2.write('controllers.py content')
    file_mock2.close()

    MyFs.popd()

    mox.ReplayAll()
    try:
        MyFs.extract_zip('modafoca.zip', base_path)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_extract_zip_verbose():
    "FileSystem.extract_zip verbose"
    mox = Mox()
    sys.stdout = StringIO()
    class MyFs(io.FileSystem):
        stack = []
        abspath = mox.CreateMockAnything()
        pushd = mox.CreateMockAnything()
        popd = mox.CreateMockAnything()
        open_raw = mox.CreateMockAnything()
        mkdir = mox.CreateMockAnything()

    mox.StubOutWithMock(io, 'zipfile')

    filename = 'modafoca.zip'
    base_path = '../to/project'
    full_path = '/full/path/to/project'

    MyFs.abspath(base_path).AndReturn(full_path)
    MyFs.pushd(full_path)

    zip_mock = mox.CreateMockAnything()

    io.zipfile.ZipFile(filename).AndReturn(zip_mock)

    file_list = [
        'settings.yml',
        'app',
        'app/controllers.py'
    ]
    zip_mock.namelist().AndReturn(file_list)
    zip_mock.read('settings.yml').AndReturn('settings.yml content')
    zip_mock.read('app/controllers.py').AndReturn('controllers.py content')

    file_mock1 = mox.CreateMockAnything()
    MyFs.open_raw('settings.yml', 'w').AndReturn(file_mock1)
    file_mock1.write('settings.yml content')
    file_mock1.close()

    MyFs.open_raw('app', 'w').AndRaise(IOError('it is a directory, dumb ass!'))
    MyFs.mkdir('app')

    file_mock2 = mox.CreateMockAnything()
    MyFs.open_raw('app/controllers.py', 'w').AndReturn(file_mock2)
    file_mock2.write('controllers.py content')
    file_mock2.close()

    MyFs.popd()

    mox.ReplayAll()
    try:
        MyFs.extract_zip('modafoca.zip', base_path, verbose=True)
        assert_equals(sys.stdout.getvalue(),
                      'Extracting files to /full/path/to/project\n  ' \
                      '-> Unpacking settings.yml\n  -> Unpacking app' \
                      '\n---> Creating directory app\n  -> Unpacking' \
                      ' app/controllers.py\n')
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
        sys.stdout = sys.__stdout__

def test_locate_non_recursive():
    "FileSystem.locate non-recursive"
    mox = Mox()

    old_glob = io.glob
    io.glob = mox.CreateMockAnything()

    base_path = '../to/project'
    full_path = '/full/path/to/project'

    class MyFs(io.FileSystem):
        stack = []
        abspath = mox.CreateMockAnything()

    io.glob('%s/*match*.py' % full_path)
    MyFs.abspath(base_path).AndReturn(full_path)
    mox.ReplayAll()
    try:
        MyFs.locate(base_path, '*match*.py', recursive=False)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
        io.glob = old_glob

def test_locate_recursive():
    "FileSystem.locate recursive"
    mox = Mox()

    base_path = '../to/project'
    full_path = '/full/path/to/project'

    class MyFs(io.FileSystem):
        stack = []
        abspath = mox.CreateMockAnything()
        walk = mox.CreateMockAnything()

    io.glob('%s/*match*.py' % full_path)
    MyFs.abspath(base_path).AndReturn(full_path)

    walk_list = [
        (None, None, ['file1.py', 'file2.jpg']),
        (None, None, ['path1/file3.png', 'path1/file4.html'])
    ]
    MyFs.walk(full_path).AndReturn(walk_list)

    mox.ReplayAll()
    try:
        MyFs.locate(base_path, '*match*.py', recursive=True)
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_mkdir_success():
    "FileSystem.mkdir with success"
    mox = Mox()

    mox.StubOutWithMock(io, 'os')

    class MyFs(io.FileSystem):
        pass

    io.os.makedirs('/make/all/those/subdirs')

    mox.ReplayAll()
    try:
        MyFs.mkdir('/make/all/those/subdirs')
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_mkdir_ignore_dirs_already_exists():
    "FileSystem.mkdir in a existent dir"
    mox = Mox()

    mox.StubOutWithMock(io, 'os')
    mox.StubOutWithMock(io.os, 'path')

    class MyFs(io.FileSystem):
        pass

    oserror = OSError()
    oserror.errno = 17

    io.os.makedirs('/make/all/those/subdirs').AndRaise(oserror)
    io.os.path.isdir('/make/all/those/subdirs').AndReturn(True)

    mox.ReplayAll()
    try:
        MyFs.mkdir('/make/all/those/subdirs')
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_mkdir_raises_on_oserror_errno_not_17():
    "FileSystem.mkdir raises on errno not 17"
    mox = Mox()

    mox.StubOutWithMock(io, 'os')
    mox.StubOutWithMock(io.os, 'path')

    class MyFs(io.FileSystem):
        pass

    oserror = OSError()
    oserror.errno = 0

    io.os.makedirs('/make/all/those/subdirs').AndRaise(oserror)

    mox.ReplayAll()
    try:

        assert_raises(OSError, MyFs.mkdir, '/make/all/those/subdirs')
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def tes_mkdir_raises_when_path_is_not_a_dir():
    "Test mkdir raises when path is not a dir"
    mox = Mox()

    mox.StubOutWithMock(io, 'os')
    mox.StubOutWithMock(io.os, 'path')

    class MyFs(io.FileSystem):
        pass

    oserror = OSError()
    oserror.errno = 17

    io.os.makedirs('/make/all/those/subdirs').AndRaise(oserror)
    io.os.isdir('/make/all/those/subdirs').AndReturn(False)
    mox.ReplayAll()
    try:
        assert_raises(OSError, MyFs.mkdir, '/make/all/those/subdirs')
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

