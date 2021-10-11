from abc import ABC
from types import MethodType

from EtherealS.Core.Model.AbstractType import AbstrackType
from EtherealS.Core.Model.AbstractTypes import AbstractTypes
from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Request.Abstract.RequestConfig import RequestConfig
from EtherealS.Core.Event import Event


def register(instance):
    from EtherealS.Request.Decorator.Request import Request
    from EtherealS.Core.Model.TrackException import ExceptionCode, TrackException
    from EtherealS.Server.Abstract.Token import Token
    for method_name in dir(instance):
        func = getattr(instance, method_name)
        if isinstance(func.__doc__, Request):
            annotation: Request = func.__doc__
            if annotation is not None:
                invoke = instance.getInvoke(func=func, annotation=annotation)
                invoke.__annotations__ = func.__annotations__
                invoke.__doc__ = func.__doc__
                invoke.__name__ = func.__name__
                setattr(instance, method_name, invoke)


class Request(ABC):

    def __init__(self):
        self.config = None
        self.name = None
        self.net_name = None
        self.exception_event = Event()
        self.log_event = Event()
        self.types = AbstractTypes()

    def OnLog(self, log: TrackLog = None, code=None, message=None):
        if log is None:
            log = TrackLog(code=code, message=message)
        log.server = self
        self.log_event.OnEvent(log=log)

    def OnException(self, exception: TrackException = None, code=None, message=None):
        if exception is None:
            exception = TrackException(code=code, message=message)
        exception.server = self
        self.exception_event.OnEvent(exception=exception)

