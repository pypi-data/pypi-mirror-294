import random
from contextlib import contextmanager
from unittest import TestCase

from thinking_modules.model import ModuleName

import thinking_tests.aspect.custom
from thinking_tests.aspect.weaving import AspectWeaver
from thinking_tests.current import current_coordinates, current_stage
from thinking_tests.outcome import Outcome
from thinking_tests.protocol import CaseCoordinates, TestStage
from thinking_tests.simple import SimpleThinkingCase


@contextmanager
def with_aspects(new_aspects):
    try:
        previous = thinking_tests.aspect.custom.CUSTOM_ASPECTS
        thinking_tests.aspect.custom.CUSTOM_ASPECTS = new_aspects
        yield
    finally:
        thinking_tests.aspect.custom.CUSTOM_ASPECTS = previous

class TestCaseAspects(TestCase):
    def setUp(self):
        self.weaver = AspectWeaver()
        self.accumulator = []
        self.setup = {"s": 1}
        self.failure = False
        self.result = random.randint(0, 0xC0FFEE)
        def s():
            self.accumulator.append(["SETUP", current_coordinates(), current_stage()])
            return self.setup

        def b(setup):
            self.accumulator.append(["BODY", current_coordinates(), current_stage(), setup])
            assert not self.failure
            return self.result
        def t(setup, outcome):
            self.accumulator.append(["TEARDOWN", current_coordinates(), current_stage(), setup, outcome])
        self.coordinates = CaseCoordinates(ModuleName.of("mock_module"), "mock_name", 123)
        self.case = SimpleThinkingCase(self.coordinates, s, b, t)

    def test_default_aspects_with_success(self):
        with self.weaver.around(TestStage.SETUP, self.case):
            s = self.case.set_up()
        self.assertEqual([["SETUP", self.coordinates, TestStage.SETUP]], self.accumulator)
        self.accumulator = []
        with self.weaver.around(TestStage.RUN, self.case):
            o = self.case.run_body(s)
        self.assertEqual(o, self.result)
        #todo add returned value, assert on resutl
        self.assertEqual([["BODY", self.coordinates, TestStage.RUN, self.setup]], self.accumulator)
        self.accumulator = []
        success = Outcome.Success()
        with self.weaver.around(TestStage.TEARDOWN, self.case):
            self.case.tear_down(s, success)
        self.assertEqual([["TEARDOWN", self.coordinates, TestStage.TEARDOWN, self.setup, success]], self.accumulator)


    def test_default_aspects_with_failure(self):
        self.failure = True
        with self.weaver.around(TestStage.SETUP, self.case):
            s = self.case.set_up()
        self.assertEqual([["SETUP", self.coordinates, TestStage.SETUP]], self.accumulator)
        self.accumulator = []
        with self.weaver.around(TestStage.RUN, self.case):
            self.assertRaises(AssertionError, lambda: self.case.run_body(s))
        self.assertEqual([["BODY", self.coordinates, TestStage.RUN, self.setup]], self.accumulator)
        self.accumulator = []
        failure = Outcome.Failure(Exception())
        with self.weaver.around(TestStage.TEARDOWN, self.case):
            self.case.tear_down(s, failure)
        self.assertEqual([["TEARDOWN", self.coordinates, TestStage.TEARDOWN, self.setup, failure]], self.accumulator)