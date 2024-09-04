from io import StringIO
from logging import StreamHandler
from typing import Self


class LogCapturer(StreamHandler):
    INSTANCE: Self = None

    def __init__(self):
        self.buffer = StringIO()
        StreamHandler.__init__(self, self.buffer)

    def get_data(self) -> str:
        return self.buffer.getvalue()

    def reset(self):
        self.buffer.seek(0)
        self.buffer.truncate(0)

LogCapturer.INSTANCE = LogCapturer()