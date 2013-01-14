import os
import sys
import commands

from tests.asserts import assert_not_equals
from lettuce.fs import FileSystem

current_directory = FileSystem.dirname(__file__)

OLD_PYTHONPATH = os.getenv('PYTHONPATH', ':'.join(sys.path))


def teardown():
    os.environ['PYTHONPATH'] = OLD_PYTHONPATH


def test_email():
    'lettuce should be able to receive emails sent from django server'
    os.environ['PYTHONPATH'] = current_directory
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoapp'

    status, out = commands.getstatusoutput(
        "django-admin.py harvest email.feature --verbosity=2")

    assert_not_equals(status, 0)
