from abc import ABC, abstractmethod

from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Service.Abstract import ServiceConfig
from EtherealS.Core import Event


class Service(ABC):
    def __init__(self):
        self.config: ServiceConfig = None
        self.methods = dict()
        self.instance = None
        self.net_name = None
        self.service_name = None
        self.exception_event: Event = Event.Event()
        self.log_event: Event = Event.Event()
        self.interceptorEvent = list()

    @abstractmethod
    def register(self, net_name, service_name, instance, config: ServiceConfig):
        pass

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

    def OnInterceptor(self, net, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(net, self, method, token):
                return False
        return True
