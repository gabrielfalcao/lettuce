from django.test.simple import DjangoTestSuiteRunner

class TestRunner(DjangoTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        super(TestRunner, self).setup_test_environment(**kwargs)
        print "Custom test runner enabled."
