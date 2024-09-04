import traceback
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from datetime import datetime
from io import StringIO
from logging import getLogger
from typing import ContextManager

from thinking_tests.aspect.protocol import TestAspect
from thinking_tests.current import test_stage
from thinking_tests.protocol import TestStage, ThinkingCase, CaseCoordinates
from thinking_tests.running.capture_logs import LogCapturer


class MetadataMountingAspect(TestAspect):
    @contextmanager
    def around(self, stage: TestStage, case: ThinkingCase) -> ContextManager:
        with test_stage(case.coordinates, stage):
            yield


class DetailsCapturingAspect(TestAspect):
    @contextmanager
    def around(self, stage: TestStage, case: ThinkingCase) -> ContextManager:
        exec_details = case.execution_details[stage]
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                LogCapturer.INSTANCE.reset()
                exec_details.started_at = datetime.now()
                yield
            except Exception as e:
                exec_details.exception = e
                raise
            finally:
                exec_details.finished_at = datetime.now()
                exec_details.stdout = stdout.getvalue()
                stdout.close()
                exec_details.stderr = stderr.getvalue()
                stderr.close()
                exec_details.logs = LogCapturer.INSTANCE.get_data()
                LogCapturer.INSTANCE.reset()
        # if stage == TestStage.TEARDOWN:
        #     case.execution_details = dict(case.execution_details)


class LogFormatter:
    def log_header(self, logger, txt):
        logger.info(txt)

    def log_footer(self, logger, success, txt):
        if success:
            logger.debug(txt)
        else:
            logger.error(txt)

    def _line(self, txt, char="=", total_len=80, pref=2, margin=" ") -> str:
        result = char*pref
        result += margin
        result += txt
        result += margin
        if len(result) < total_len:
            result += char*(total_len - len(result))
        return result

    def _stage(self, s: TestStage) -> str:
        match s:
            case TestStage.SETUP: return "Setup of"
            case TestStage.RUN: return "Running"
            case TestStage.TEARDOWN: return "Teardown of"
    def make_header(self, coordinates: CaseCoordinates, stage: TestStage) -> str:
        return self._line(f"{self._stage(stage)} {coordinates.id}")

    def make_success_footer(self, coordinates: CaseCoordinates, stage: TestStage) -> str:
        return self._line(f"{self._stage(stage)} {coordinates.id}", char="-")

    def make_exception_footer(self, coordinates: CaseCoordinates, stage: TestStage, e: BaseException) -> list[str]:
        return [
            self._line(f"{self._stage(stage)} {coordinates.id}", char="-"),
        ] + [
            x.rstrip() for x in traceback.format_exception(e)
        ] + [
            self._line(f"{self._stage(stage)} {coordinates.id}", char="-"),
        ]


BEFORE_AFTER_LOG_FORMATER = LogFormatter()

class LoggingAspect(TestAspect):
    @contextmanager
    def around(self, stage: TestStage, case: ThinkingCase) -> ContextManager:
        logger = getLogger(case.coordinates.module_name.qualified)
        fmt = BEFORE_AFTER_LOG_FORMATER
        try:
            fmt.log_header(logger, fmt.make_header(case.coordinates, stage))
            yield
            fmt.log_footer(logger, True, fmt.make_success_footer(case.coordinates, stage))
        except BaseException as e:
            for line in fmt.make_exception_footer(case.coordinates, stage, e):
                fmt.log_footer(logger, False, line)
            raise



DEFAULT_ASPECTS = [
    MetadataMountingAspect(),
    DetailsCapturingAspect(),
    LoggingAspect()
]