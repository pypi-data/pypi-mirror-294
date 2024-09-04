import traceback
from abc import abstractmethod
from contextlib import contextmanager
from typing import TypeVar

from coverage import Coverage

import thinking_tests.forks.junit_xml as junit_xml
from thinking_tests.forks.vjunit import VJunit
from thinking_tests.protocol import ThinkingCase, ThinkingSuite, TestStage, ResultType
from thinking_tests.running.test_config import test_config

BackendResultType = TypeVar("BackendResultType")

class ThinkingTestRunner:
    @abstractmethod
    def execute_suite(self, cases: ThinkingSuite) -> BackendResultType: pass

    def execute(self, cases: list[ThinkingCase]) -> BackendResultType:
        suite = ThinkingSuite.build(cases)
        ctx = self._coverage() if test_config.coverage.enabled else self._noop()
        with ctx:
            result = self.execute_suite(suite)
        if test_config.unittest.xml_report_enabled:
            self._prepare_xml_report(suite, test_config.unittest.xml_report_path)
        if test_config.unittest.html_report_enabled:
            VJunit().convert(test_config.unittest.xml_report_path, test_config.unittest.html_report_path)
        #todo html report
        return result

    def _prepare_xml_report(self, suite: ThinkingSuite, report_path: str):
        def xcase(case: ThinkingCase) -> junit_xml.TestCase:
            out = junit_xml.TestCase(
                case.coordinates.id,
                case.coordinates.module_name.qualified+"."+case.coordinates.name,
                case.duration.total_seconds(),
                case.stdout,
                case.stderr,
                timestamp=case.execution_details[TestStage.SETUP].started_at,
                file=case.coordinates.module_name.module_descriptor.file_path,
                line=case.coordinates.lineno,
                log=case.logs
            )
            def _exc_to_info(e):
                return repr(e), traceback.format_exception(e), type(e).__name__
            if case.result_type == ResultType.ERROR:
                out.add_error_info(*_exc_to_info(case.error_exception))
            elif case.result_type == ResultType.FAILURE:
                out.add_failure_info(*_exc_to_info(case.failure_exception))
            return out
        def xsuite(suite: ThinkingSuite) -> junit_xml.TestSuite:
            out = junit_xml.TestSuite(
                suite.module_name.qualified,
                [
                    xcase(c)
                    for c in suite.tests
                ],
                file=suite.module_name.module_descriptor.file_path,
                suites=[xsuite(s) for s in suite.suites]
            )
            p = suite.module_name.parent
            if p is not None:
                out.package = p.qualified
            return out
        with open(report_path, "w") as f:
            junit_xml.to_xml_report_file(f, [xsuite(suite)])

    @contextmanager
    def _noop(self):
        yield

    @contextmanager
    def _coverage(self):
        try:
            yield
        finally:
            # cov.stop()
            coverage_instance = Coverage.current()
            if coverage_instance:
                coverage_instance.save()
                if test_config.coverage.xml_report_enabled:
                    coverage_instance.xml_report(coverage_instance.get_data().measured_files(), test_config.coverage.xml_report_path)
                if test_config.coverage.html_report_enabled:
                    coverage_instance.html_report(coverage_instance.get_data().measured_files(), test_config.coverage.html_report_dir)
            else:
                assert not test_config.coverage.binary_report_enabled

    def run(self, case: ThinkingCase) -> BackendResultType:
        return self.execute([case])

