from abc import ABC, abstractmethod

from autobahn.twisted import WebSocketServerFactory

from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Core.Event import Event


class Server(ABC, WebSocketServerFactory):

    def __init__(self, prefixes, create_method, config):
        super().__init__()
        self.config = config
        self.net_name = None
        self.exception_event = Event()
        self.log_event = Event()
        self.prefixes = prefixes
        self.create_method = create_method

    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def Close(self):
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
