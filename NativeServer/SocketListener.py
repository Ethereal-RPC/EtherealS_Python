import sys
from typing import Tuple

from twisted.internet import reactor
from twisted.internet.defer import log
from twisted.internet.protocol import ServerFactory

from NativeServer.DataToken import DataToken
from RPCService.ServiceConfig import ServiceConfig


class SocketListener(ServerFactory):
    # 指向一个协议类,我们自定义的
    config: ServiceConfig
    server_key: (str, str) = None

    def __init__(self, server_key, config: ServiceConfig):
        self.server_key = server_key
        self.config = config

    def buildProtocol(self, addr: Tuple[str, int]) -> "Protocol":
        return DataToken(self.server_key, self.config)

    def Run(self):
        reactor.listenTCP(self.server_key[0], SocketListener(self.server_key, self.ServiceConfig))
        reactor.run()


# 配置将日志输出到stdout
log.startLogging(sys.stdout)
