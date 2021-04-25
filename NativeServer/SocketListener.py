import json
from typing import Tuple
from twisted.internet import reactor
from twisted.internet.interfaces import ITransport
from twisted.internet.protocol import ServerFactory

from Model.BaseUserToken import BaseUserToken
from Model.ClientResponseModel import ClientResponseModel
from Model.RPCException import RPCException
from Model.ServerRequestModel import ServerRequestModel
from NativeServer.DataToken import DataToken
from NativeServer.ServerConfig import ServerConfig
from RPCNet import NetCore
from Utils import JsonTool


class SocketListener(ServerFactory):

    def __init__(self, server_key, config: ServerConfig):
        self.server_key = server_key
        self.config = config
        net_config = NetCore.Get(server_key)
        if net_config is None:
            raise RPCException(RPCException.ErrorCode.RegisterError, "{0}找不到NetConfig".format(server_key))
        net_config.serverRequestSend = self.SendServerRequest
        net_config.clientResponseSend = self.SendClientResponse

    def buildProtocol(self, addr: Tuple[str, int]) -> "Protocol":
        return DataToken(self.server_key, self.config)

    def run(self):
        reactor.listenTCP(int(self.server_key[1]), self)
        reactor.run()

    def SendClientResponse(self, token: BaseUserToken, response: ClientResponseModel):
        transport: ITransport = token.net
        if transport is not None:
            body = self.config.clientResponseModelSerialize(response).encode(self.config.encode)
            content = bytearray()
            content.extend(body.__len__().to_bytes(4, "little"))
            content.extend(int.to_bytes(1, 1, "little"))
            content.extend(bytes(27))
            content.extend(body)
            transport.write(content)

    def SendServerRequest(self, token: BaseUserToken, request: ServerRequestModel):
        transport: ITransport = token.net
        if transport is not None:
            body = self.config.serverRequestModelSerialize(request).encode(self.config.encode)
            content = bytearray()
            content.extend(body.__len__().to_bytes(4, "little"))
            content.extend(int.to_bytes(0, 1, "little"))
            content.extend(bytes(27))
            content.extend(body)
            transport.write(content)
