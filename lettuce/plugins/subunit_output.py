

from lettuce.terrain import before, after

from subunit.v2 import StreamResultToBytes

def open_file(filename):
    """
    open a subunit file

    this is not a context manager because it is used asynchronously by
    hooks
    
    out of the scope of enable() because we want to patch it in our tests
    """

    filename = filename or 'subunit.bin'

    return open(filename, 'wb')


def close_file(file_):
    """
    """

    file_.close()


def enable(filename=None):

    file_ = open_file(filename)

    streamresult = StreamResultToBytes(file_)
    streamresult.startTestRun()

    @before.each_scenario
    def before_scenario(scenario):

        streamresult.status(test_id=get_test_id(scenario),
                            test_status='inprogress')

    @after.each_scenario
    def after_scenario(scenario):

        if scenario.passed:
            streamresult.status(test_id=get_test_id(scenario),
                                test_status='success')
        else:
            streamresult.status(test_id=get_test_id(scenario),
                                test_status='fail')

    @after.all
    def after_all(total):
        streamresult.stopTestRun()
        close_file(file_)


def get_test_id(scenario):
    return '{} {}'.format(scenario.feature.name, scenario.name)
