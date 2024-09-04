from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Protocol, TypeVar, NamedTuple, runtime_checkable, Self, Optional, Any

from thinking_modules.model import ModuleName

from thinking_tests.outcome import Outcome

Setup = TypeVar("Setup")
Result = TypeVar("Result")


class TestStage(Enum):
    SETUP = auto()
    RUN = auto()
    TEARDOWN = auto()

class CaseCoordinates(NamedTuple):
    module_name: ModuleName
    name: str
    lineno: int

    @property
    def id(self) -> str:
        # return f"{self.module_name} ({self.lineno}) :: ${self.name}"
        return f"{self.module_name.qualified}[{self.lineno}] :: {self.name}"

class ResultType(Enum):
    SUCCESS = auto()
    ERROR = auto()
    FAILURE = auto()

@dataclass
class StageExecutionDetails:
    stdout: str = None
    stderr: str = None
    logs: str = None
    started_at: datetime = None
    finished_at: datetime = None
    exception: Exception = None

    @property
    def duration(self) -> Optional[timedelta]:
        if self.started_at is not None and self.finished_at is not None:
            return self.finished_at - self.started_at
        return None

@runtime_checkable
class ThinkingCase(Protocol):
    coordinates: CaseCoordinates
    execution_details: dict[TestStage, StageExecutionDetails]

    @abstractmethod
    def set_up(self) -> Setup: pass

    @abstractmethod
    def run_body(self, setup: Setup) -> Any: pass

    @abstractmethod
    def tear_down(self, setup: Setup, outcome: Outcome): pass

    def run(self):
        from thinking_tests.runner.run import run
        return run(self)

    def __call__(self):
        return self.run()

    @property
    def duration(self) -> timedelta:
        out = timedelta()
        for stage in TestStage:
            d = self.execution_details[stage].duration
            if d is None:
                return out
            out += d
        return out

    @property
    def result_type(self) -> ResultType:
        if self.error_exception is not None:
            return ResultType.ERROR
        if self.failure_exception is not None:
            return ResultType.FAILURE
        return ResultType.SUCCESS

    @property
    def error_exception(self) -> Optional[Exception]:
        return self.execution_details[TestStage.SETUP].exception or self.execution_details[TestStage.TEARDOWN].exception

    @property
    def failure_exception(self) -> Optional[Exception]:
        return self.execution_details[TestStage.RUN].exception

    @property
    def stdout(self) -> str:
        return "\n\n".join( self.execution_details[s].stdout for s in TestStage if self.execution_details[s].stdout)

    @property
    def stderr(self) -> str:
        return "\n\n".join( self.execution_details[s].stderr for s in TestStage if self.execution_details[s].stderr)

    @property
    def logs(self) -> str:
        return "\n\n".join( self.execution_details[s].logs for s in TestStage if self.execution_details[s].logs)

@dataclass
class ThinkingSuite:
    module_name: ModuleName = None
    tests: list[ThinkingCase] = field(default_factory=list)
    suites: list[Self] = field(default_factory=list)

    def at(self, *parts: str) -> Self:
        if len(parts):
            first = parts[0]
            rest = parts[1:]
            try:
                sub = self.named(first)
            except KeyError:
                sub = ThinkingSuite()
                self.set(first, sub)
            return sub.at(*rest)
        else:
            return self

    def named(self, suite_name: str) -> Self:
        for s in self.suites:
            if s.name == suite_name:
                return s
        raise KeyError()

    def set(self, suite_name: str, suite: Self):
        if suite.name is None:
            suite.name = suite_name
        else:
            assert suite.name == suite_name #todo msg
        for i, s in enumerate(self.suites):
            if s.name == suite_name:
                self.suites[i] = suite
                return
        self.suites.append(suite)

    @property
    def duration(self) -> timedelta:
        out = timedelta()
        for t in self.tests:
            out += t.duration
        return out

    @property
    def total_duration(self) -> timedelta:
        out = self.duration
        for suite in self.suites:
            out += suite.total_duration
        return out

    @property
    def errors(self) -> list[ThinkingCase]:
        return [ t for t in self.tests if t.result_type == ResultType.ERROR ]

    @property
    def failures(self) -> list[ThinkingCase]:
        return [t for t in self.tests if t.result_type == ResultType.FAILURE]

    @property
    def successes(self) -> list[ThinkingCase]:
        return [t for t in self.tests if t.result_type == ResultType.SUCCESS]

    @property
    def all_errors(self) -> list[ThinkingCase]:
        out = self.errors
        for suite in self.suites:
            out += suite.all_errors
        return out

    @property
    def all_failures(self) -> list[ThinkingCase]:
        out = self.failures
        for suite in self.suites:
            out += suite.all_failures
        return out


    @property
    def all_successes(self) -> list[ThinkingCase]:
        out = self.successes
        for suite in self.suites:
            out += suite.all_successes
        return out

    @classmethod
    def build(cls, cases: list[ThinkingCase]) -> Self:
        #fixme ModuleName is not hashable - make parts a tuple and you'll be good
        mod_to_suite: dict[ModuleName, ThinkingSuite] = {}
        def suite_for_module(m: ModuleName) -> ThinkingSuite:
            q = m.qualified
            if q not in mod_to_suite:
                s = ThinkingSuite(m)
                mod_to_suite[q] = s
                p = m.parent
                if p is not None:
                    ps = suite_for_module(p)
                    ps.suites.append(s)
                return s
            return mod_to_suite[q]
        for c in cases:
            mod = c.coordinates.module_name
            suite_for_module(mod).tests.append(c)
        parentless = [ mod_to_suite[m.qualified] for m in map(ModuleName.of, mod_to_suite.keys()) if m.parent is None ]
        if len(parentless) == 1:
            return parentless[0]
        return ThinkingSuite(suites=parentless)
