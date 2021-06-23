from Model.BaseUserToken import BaseUserToken
from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from Model.RPCTypeConfig import RPCTypeConfig
from RPCService import Service
from Utils.Event import Event


class ServiceConfig:

    def __init__(self, _type: RPCTypeConfig):
        self.types: RPCTypeConfig = _type
        self.interceptorEvent = list()
        self.authoritable = False
        self.exception_event = Event()
        self.log_event = Event()

    def OnInterceptor(self, service: Service, method: classmethod, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            item: method
            if not item.__call__(service, method, token):
                return False
        return True

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        service = kwargs.get("service")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.onEvent(log=log, service=service)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        service = kwargs.get("service")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.onEvent(exception=exception, service=service)
        raise exception
