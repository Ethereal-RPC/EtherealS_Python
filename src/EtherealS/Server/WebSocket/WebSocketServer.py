import threading
from abc import abstractmethod
from urllib.parse import urlparse

from autobahn.twisted import WebSocketServerFactory

from EtherealS.Server.Abstract.Server import Server
from EtherealS.Server.Abstract.ServerConfig import ServerConfig
from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Server.WebSocket.TokenProtocol import TokenProtocol
from EtherealS.Server.WebSocket.WebSocketServerConfig import WebSocketServerConfig


class WebSocketServer(Server, WebSocketServerFactory):

    def __init__(self, prefixes: list):
        Server.__init__(self,prefixes)
        WebSocketServerFactory.__init__(self)
        self.config = WebSocketServerConfig()
        self.setProtocolOptions()
        self.protocol = self.getProtocol

    def getProtocol(self):
        return TokenProtocol(self.net.name)

    def Start(self):
        try:
            from twisted.internet import reactor
            reactor.listenTCP(urlparse(self.prefixes[0].replace("ethereal://", "ws://")).port, self)
        except Exception as e:
            self.OnException(exception=TrackException(exception=e))

    def Close(self):
        self.doStop()
