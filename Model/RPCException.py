from enum import Enum


class ErrorCode(Enum):
    RegisterError = 1
    RuntimeError = 2


class RPCException(Exception):
    ErrorCode = ErrorCode.RegisterError

    def __init__(self, code, msg):
        super().__init__(code, msg)
