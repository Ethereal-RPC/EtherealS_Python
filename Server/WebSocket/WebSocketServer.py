from abc import abstractmethod
from urllib.parse import urlparse

from autobahn.twisted import WebSocketServerFactory
from twisted.internet import reactor

from Server.Abstract.Server import Server
from Server.Abstract.ServerConfig import ServerConfig


class WebSocketServer(Server, WebSocketServerFactory):

    def __init__(self, net, prefixes, config: ServerConfig):
        super().__init__(net, config)
        self.setProtocolOptions()
        self.prefixes = prefixes
        self.protocol = self.getProtocol

    def getProtocol(self):
        token = self.config.create_method()
        token.config = self.config
        token.net_name = self.net_name
        token.prefixes = self.prefixes
        token.log_event.Register(self.OnLog)
        token.exception_event.Register(self.OnException)
        return token

    def Start(self):
        try:
            reactor.listenTCP(urlparse("ws://" + self.prefixes).port, self)
            reactor.run()
        except Exception as e:
            self.OnException(exception=e)

    def Close(self):
        pass
