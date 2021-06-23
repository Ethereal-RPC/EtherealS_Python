from enum import Enum


class ErrorCode(Enum):
    Core = 1
    Runtime = 2


class RPCException(Exception):

    def __init__(self, code: ErrorCode, message):
        super().__init__(code, message)
        self.ErrorCode = ErrorCode.Core
        self.message = message
