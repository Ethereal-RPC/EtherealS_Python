from abc import ABC, abstractmethod

from EtherealS.Core.BaseCore.BaseCore import BaseCore
from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Core.Model import ServerRequestModel
from EtherealS.Service import ServiceCore
from EtherealS.Core.Event import Event


class Token(ABC,BaseCore):
    def __init__(self):
        super().__init__()
        self.key = None
        self.service = None
        self.connect_event = Event()
        self.disconnect_event = Event()

    def Register(self, replace=False):
        tokens = self.service.tokens
        if tokens is not None:
            if replace is False:
                if tokens.get(self.key, None) is not None:
                    return True
            tokens[self.key] = self
            return True

    def UnRegister(self):
        tokens = self.service.tokens
        if tokens.get(self.key, None) is not None:
            del tokens[self.key]
        return True

    def GetTokens(self):
        tokens = self.service.tokens
        return tokens

    def GetToken(self, key):
        tokens = self.service.tokens
        return tokens.get(key, None)

    @abstractmethod
    def SendClientResponse(self, response: ClientResponseModel):
        pass

    @abstractmethod
    def SendServerRequest(self, request: ServerRequestModel):
        pass

    @abstractmethod
    def serialize(self):
        pass

    def OnSuccessConnect(self):
        self.connect_event.OnEvent(token=self)

    def OnDisConnect(self):
        self.disconnect_event.OnEvent(token=self)
