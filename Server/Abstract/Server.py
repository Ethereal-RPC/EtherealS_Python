from abc import ABC, abstractmethod

from autobahn.twisted import WebSocketServerFactory

from Core.Model.TrackException import TrackException
from Core.Model.TrackLog import TrackLog
from Server.Abstract.ServerConfig import ServerConfig
from Core.Event import Event


class Server(ABC, WebSocketServerFactory):

    def __init__(self, net_name, config: ServerConfig):
        super().__init__()
        self.config = config
        self.net_name = net_name
        self.exception_event = Event()
        self.log_event = Event()

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
