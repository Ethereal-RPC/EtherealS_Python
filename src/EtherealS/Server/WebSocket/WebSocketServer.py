import threading
from abc import abstractmethod
from urllib.parse import urlparse

from autobahn.twisted import WebSocketServerFactory

from EtherealS.Server.Abstract.Server import Server
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Server.WebSocket.WebSocketServerConfig import WebSocketServerConfig


class WebSocketServer(Server, WebSocketServerFactory):

    def __init__(self, prefixes: list, create_method):
        super().__init__(prefixes=prefixes, create_method=create_method)
        self.config = WebSocketServerConfig()
        self.setProtocolOptions()
        self.protocol = self.getProtocol

    def getProtocol(self):
        token = self.create_method()
        token.config = self.config
        token.net = self.net
        token.prefixes = self.prefixes
        token.log_event.Register(self.OnLog)
        token.exception_event.Register(self.OnException)
        return token

    def Start(self):
        try:
            from twisted.internet import reactor
            reactor.listenTCP(urlparse(self.prefixes[0].replace("ethereal://", "ws://")).port, self)
        except Exception as e:
            self.OnException(exception=TrackException(exception=e))

    def Close(self):
        self.doStop()
