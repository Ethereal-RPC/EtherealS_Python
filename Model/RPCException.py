from enum import Enum


class ExceptionCode(Enum):
    Core = 1,
    Runtime = 2


class RPCException(Exception):

    def __init__(self, code: ExceptionCode, message):
        super().__init__(code, message)
        self.ErrorCode = ExceptionCode.Core
        self.message = message
