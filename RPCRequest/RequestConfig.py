from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from Model.RPCTypeConfig import RPCTypeConfig
from Utils.Event import Event


class RequestConfig:

    def __init__(self, config_type: RPCTypeConfig):
        self.types = config_type
        self.tokenEnable: bool = True
        self.exception_event = Event()
        self.log_event = Event()

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        request = kwargs.get("request")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.onEvent(log=log, request=request)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        request = kwargs.get("request")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.onEvent(exception=exception, request=request)
        raise exception
