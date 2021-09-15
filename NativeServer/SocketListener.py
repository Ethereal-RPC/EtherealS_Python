from urllib.parse import urlparse

from autobahn.twisted import WebSocketServerFactory
from twisted.internet import reactor

from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from NativeServer.ServerConfig import ServerConfig
from Utils.Event import Event


class SocketListener(WebSocketServerFactory):

    def __init__(self, net, prefixes, config: ServerConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProtocolOptions()
        self.prefixes = prefixes
        self.config = config
        self.net_name = net.name
        self.exception_event = Event()
        self.log_event = Event()
        self.protocol = self.getProtocol

    def getProtocol(self):
        token = self.config.create_method()
        token.config = self.config
        token.net_name = self.net_name
        token.prefixes = self.prefixes
        token.log_event.Register(self.OnLog)
        token.exception_event.Register(self.OnException)
        return token

    def start(self):
        try:
            reactor.listenTCP(urlparse("ws://" + self.prefixes).port, self)
            reactor.run()
        except Exception as exception:
            self.OnException(exception=exception)

    def OnLog(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        server = kwargs.get("server")
        log = kwargs.get("log")
        if log is None:
            log = RPCLog(code, message)
        self.log_event.OnEvent(log=log, server=server)

    def OnException(self, **kwargs):
        code = kwargs.get("code")
        message = kwargs.get("message")
        exception = kwargs.get("exception")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.OnEvent(exception=exception, server=self)
