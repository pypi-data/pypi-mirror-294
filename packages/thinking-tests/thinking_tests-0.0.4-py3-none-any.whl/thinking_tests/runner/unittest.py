from unittest import TextTestRunner, TestSuite, TestResult, TestCase

from thinking_tests.adapter import adapt
from thinking_tests.protocol import ThinkingCase
from thinking_tests.runner.protocol import ThinkingTestRunner, ThinkingSuite


class UnittestRunner(ThinkingTestRunner):
    def __init__(self, unittest_runner = None):
        self.backend = unittest_runner or TextTestRunner()
        # self.backend = unittest_runner or XMLTestRunner()

    def execute_suite(self, suite: ThinkingSuite) -> TestResult:
        backend_suite = self._make_suite(suite)
        return self.backend.run(backend_suite)

    def _make_suite(self, suite: ThinkingSuite) -> TestSuite:
        def to_test(t: ThinkingCase) -> TestCase:
            return adapt(t)
        def to_suite(s: ThinkingSuite) -> TestSuite:
            return TestSuite([to_test(x) for x in s.tests] + [to_suite(x) for x in s.suites])
        return to_suite(suite)

    # def _make_suite(self, cases: ThinkingSuite) -> TestSuite:
    #
    #     return TestSuite([adapt(case) for case in cases])
