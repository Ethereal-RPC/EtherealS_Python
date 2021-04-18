from enum import Enum


class ErrorCode(Enum):
    RegisterError = 1
    RuntimeError = 2


class RPCException(Exception):

    def __init__(self, code: ErrorCode, msg):
        super().__init__(code, msg)
        self.ErrorCode = ErrorCode.RegisterError
