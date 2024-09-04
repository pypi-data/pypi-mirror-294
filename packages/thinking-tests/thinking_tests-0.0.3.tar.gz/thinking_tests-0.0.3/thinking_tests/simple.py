import inspect
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Callable, TypeVar

from thinking_tests.outcome import Outcome, ResultType
from thinking_tests.protocol import ThinkingCase, Setup, CaseCoordinates, StageExecutionDetails, TestStage

T = TypeVar("T")

def _describe_args(callable: Callable) -> list[str]:
    return inspect.getargs(callable.__code__).args

def _bind_args(args: list[str], bindings: dict[str, object]) -> tuple:
    return tuple([bindings.get(k) for k in args])

@dataclass
class SimpleThinkingCase(ThinkingCase):
    coordinates: CaseCoordinates

    setup: Callable[[], Setup]
    body: Callable[[...], ResultType]
    teardown: Callable[[...], Outcome | ResultType]

    execution_details: dict[TestStage, StageExecutionDetails] = field(default_factory=lambda: defaultdict(StageExecutionDetails))

    def set_up(self) -> Setup:
        with self._store_exceptions(TestStage.SETUP):
            return self.setup()


    def run_body(self, setup: Setup) -> Outcome:
        args = _describe_args(self.body)

        bound = _bind_args(args, {"setup": setup})
        with self._store_exceptions(TestStage.RUN):
            return self.body(*bound)


    def tear_down(self, setup: Setup, outcome: Outcome) -> Outcome:
        with self._store_exceptions(TestStage.TEARDOWN):
            args = _describe_args(self.teardown)
            bound = _bind_args(args, {"setup": setup, "outcome": outcome})
            result = self.teardown(*bound)
            if result is None: return outcome
            if isinstance(result, Outcome): return result
            return outcome

    @contextmanager
    def _store_exceptions(self, stage):
        try:
            yield
        except Exception as e:
            self.execution_details[stage].exception = e
            raise




