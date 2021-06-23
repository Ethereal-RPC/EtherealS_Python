from Model.BaseUserToken import BaseUserToken
from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from RPCService.Service import Service
from Utils.Event import Event


class NetConfig:

    def __init__(self):
        self.interceptorEvent = list()
        self.exception_event = Event()
        self.log_event = Event()

    def OnInterceptor(self, service: Service, method, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(service, method, token):
                return False
        return True

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        net = kwargs.get("net")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.onEvent(log=log, net=net)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        net = kwargs.get("net")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.onEvent(exception=exception, net=net)
        raise exception

