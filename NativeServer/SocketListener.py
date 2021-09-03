import json
from typing import Tuple

from twisted.internet import reactor
from twisted.internet.interfaces import ITransport
from twisted.internet.protocol import ServerFactory

from Model.BaseUserToken import BaseUserToken
from Model.ClientResponseModel import ClientResponseModel
from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from Model.ServerRequestModel import ServerRequestModel
from NativeServer.DataToken import DataToken
from NativeServer.ServerConfig import ServerConfig
from RPCNet.Net import Net
from Utils.Event import Event


class SocketListener(ServerFactory):

    def __init__(self, net: Net, server_key, config: ServerConfig):
        self.server_key = server_key
        self.config = config
        self.net_name = net.name
        self.exception_event = Event()
        self.log_event = Event()
        net.serverRequestSend = self.SendServerRequest
        net.clientResponseSend = self.SendClientResponse

    def buildProtocol(self, addr: Tuple[str, int]) -> "Protocol":
        return DataToken(self.net_name, self.server_key, self.config)

    def start(self):
        try:
            reactor.listenTCP(int(self.server_key[1]), self)
            reactor.run()
        except Exception as exception:
            self.OnException(exception=exception)

    def SendClientResponse(self, token: BaseUserToken, response: ClientResponseModel):
        transport: ITransport = token.net
        if transport is not None:
            body = self.config.clientResponseModelSerialize(response).encode(self.config.encode)
            content = bytearray()
            content.extend(body.__len__().to_bytes(4, "little"))
            content.extend(int.to_bytes(1, 1, "little"))
            content.extend(bytes(27))
            content.extend(body)
            # 后期可以试着解决一下二次复制的问题
            transport.write(bytes(content))

    def SendServerRequest(self, token: BaseUserToken, request: ServerRequestModel):
        transport: ITransport = token.net
        if transport is not None:
            body = self.config.serverRequestModelSerialize(request).encode(self.config.encode)
            content = bytearray()
            content.extend(body.__len__().to_bytes(4, "little"))
            content.extend(int.to_bytes(0, 1, "little"))
            content.extend(bytes(27))
            content.extend(body)
            # 后期可以试着解决一下二次复制的问题
            transport.write(bytes(content))

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
        server = kwargs.get("server")
        if exception is None:
            exception = RPCException(code, message)
        self.exception_event.OnEvent(exception=exception, server=server)
        raise exception