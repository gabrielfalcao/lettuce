"""Make sure after.each_step, after.outline, after.each_scenario, and
after_each feature hooks are invoked, regardless of whether a test passes.
"""

from mock import MagicMock
from lettuce import Runner, after
from nose.tools import assert_equals, assert_raises, with_setup
from os.path import dirname, join, abspath
from tests.asserts import prepare_stdout, prepare_stderr

def define_hooks(mock):
    @after.each_feature    
    def after_each_feature(feature):
        mock.after_each_feature()

    @after.each_scenario    
    def after_each_scenario(scenario):
        mock.after_each_scenario()

    @after.each_step    
    def after_each_step(step):
        mock.after_each_step()

    @after.outline    
    def after_outline(scenario, order, outline, reasons_to_fail):
        mock.after_outline()

def get_after_hook_mock():
    mock = MagicMock()
    mock.after_each_feature = MagicMock()
    mock.after_each_scenario = MagicMock()
    mock.after_each_step = MagicMock()
    mock.after_outline = MagicMock()
    return mock

current_dir = abspath(dirname(__file__))
ojoin = lambda *x: join(current_dir, 'output_features', *x)
def joiner(callback, name):
    return callback(name, "%s.feature" % name)
feature_name = lambda name: joiner(ojoin, name)

def run_feature(feature, feature_will_fail, failfast,
             after_each_feature_count, after_each_scenario_count,
             after_each_step_count, after_outline_count):
    mock = get_after_hook_mock()
    define_hooks(mock)
    runner = Runner(feature_name(feature), failfast=failfast) 
    if feature_will_fail:
        try:
            runner.run()
        except:
            pass
    else:
        runner.run()
    assert_equals(mock.after_each_feature.call_count, after_each_feature_count)
    assert_equals(mock.after_each_scenario.call_count, after_each_scenario_count)
    assert_equals(mock.after_each_step.call_count, after_each_step_count)
    assert_equals(mock.after_outline.call_count, after_outline_count)

@with_setup(prepare_stdout)
def test_success_outline():
    run_feature('success_outline', False, False, 1, 1, 24, 3)

@with_setup(prepare_stdout)
def test_success_outline_failfast():
    run_feature('success_outline', False, True, 1, 1, 24, 3)

@with_setup(prepare_stdout)
def test_fail_outline():
    run_feature('fail_outline', True, False, 1, 1, 24, 3)

@with_setup(prepare_stdout)
def test_fail_outline_failfast():
    run_feature('fail_outline', True, True, 1, 1, 12, 2)

@with_setup(prepare_stdout)
def test_success_non_outline():
    run_feature('success_table', False, False, 1, 1, 5, 0)

@with_setup(prepare_stdout)
def test_success_non_outline_failfast():
    run_feature('success_table', False, True, 1, 1, 5, 0)

@with_setup(prepare_stdout)
def test_fail_non_outline():
    run_feature('failed_table', True, False, 1, 1, 5, 0)

@with_setup(prepare_stdout)
def test_fail_non_outline_failfast():
    run_feature('failed_table', True, True, 1, 1, 2, 0)

@with_setup(prepare_stderr)
@with_setup(prepare_stdout)
def test_fail_system_exiting_non_outline():
    run_feature('system_exiting_error', True, False, 1, 1, 1, 0)

@with_setup(prepare_stdout)
def test_fail_system_exiting_failfast_non_outline():
    run_feature('system_exiting_error', True, True, 1, 1, 1, 0)

