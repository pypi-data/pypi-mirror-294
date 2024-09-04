from dataclasses import dataclass

from thinking_runtime.bootstrap import bootstrap
from thinking_runtime.defaults.logging_config import logging_config, RawHandler
from thinking_runtime.setup import register_action

from thinking_tests.running.capture_logs import LogCapturer
from thinking_tests.running.test_setup_action import SetupTests

TEST_LOG_CAPTURE_NAME = "Test log capture"

def bootstrap_tests():
#fixme RawHandler is not dataclass! silly me
    logging_config.handlers.raw.append(dataclass(RawHandler)(TEST_LOG_CAPTURE_NAME, LogCapturer.INSTANCE))

    register_action(SetupTests)

    bootstrap()