from autobahn.twisted import WebSocketServerProtocol
from autobahn.websocket import protocol

from EtherealS.Core.Model import ClientRequestModel
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.Error import Error, ErrorCode
from EtherealS.Core.Model.TrackLog import LogCode
from EtherealS.Core.Model import ServerRequestModel
from EtherealS.Service.Abstract.Token import Token


class WebSocketToken(Token):

    def SendClientResponse(self, response: ClientResponseModel):
        pass

    def SendServerRequest(self, request: ServerRequestModel):
        pass

    def serialize(self):
        pass
