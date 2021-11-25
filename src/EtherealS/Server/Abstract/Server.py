from abc import ABC, abstractmethod

from autobahn.twisted import WebSocketServerFactory

from EtherealS.Core.BaseCore.BaseCore import BaseCore
from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Core.Event import Event


class Server(ABC,BaseCore):

    def __init__(self, prefixes):
        BaseCore.__init__(self)
        self.config = None
        self.net = None
        self.prefixes: list = prefixes

    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def Close(self):
        pass
