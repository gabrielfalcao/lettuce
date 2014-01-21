"""
Utils for testing
"""
import commands
from functools import wraps
from lettuce.fs import FileSystem


def run_scenario(application='', feature='', scenario='', **opts):
    """
    Runs a Django scenario and returns it's output vars
    """
    if application:
        application = ' {0}/features/'.format(application)

    if feature:
        feature = '{0}.feature'.format(feature)

    if scenario:
        scenario = ' -s {0:d}'.format(scenario)

    opts_string = ''
    for opt, val in opts.iteritems():
        if not val:
            val = ''

        opts_string = ' '.join((opts_string, opt, val))

    cmd = 'python manage.py harvest -v 3 -T {0}{1}{2}{3}'.format(opts_string,
                                                                 application,
                                                                 feature,
                                                                 scenario,
                                                                 )
    return commands.getstatusoutput(cmd)


def in_directory(*directories):
    """
    Decorator to set the working directory around a function
    """
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            FileSystem.pushd(*directories)
            value = func(*args, **kwargs)
            FileSystem.popd()
            return value
        return inner
    return decorator
