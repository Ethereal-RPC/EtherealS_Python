from enum import Enum


class ExceptionCode(Enum):
    Core = 1,
    Runtime = 2


class TrackException(Exception):

    def __init__(self, code: ExceptionCode, message):
        super().__init__(code, message)
        self.code = ExceptionCode.Core
        self.message = message
        self.exception = None
        self.server = None
        self.net = None
        self.request = None
        self.service = None
