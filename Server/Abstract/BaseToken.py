from abc import ABC, abstractmethod

from autobahn.twisted import WebSocketServerProtocol
from autobahn.websocket import protocol

from Core.Model import ClientRequestModel
from Core.Model.ClientResponseModel import ClientResponseModel
from Core.Model.Error import Error, ErrorCode
from Core.Model.TrackException import TrackException
from Core.Model.TrackLog import TrackLog, LogCode
from Core.Model import ServerRequestModel
from Net import NetCore
from Net.Abstract.Net import Net
from Core.Event import Event


class BaseToken(ABC, WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self.key = None
        self.config = None
        self.net_name = None
        self.exception_event = Event()
        self.log_event = Event()
        self.connect_event = Event()
        self.disconnect_event = Event()

    def Register(self, replace=False):
        net: Net = NetCore.Get(self.net_name)
        tokens = net.tokens
        if tokens is not None:
            if replace is False:
                if tokens.get(self.key, None) is not None:
                    return True
            tokens[self.key] = self
            return True

    def UnRegister(self):
        net: Net = NetCore.Get(self.net_name)
        tokens = net.tokens
        if tokens.get(self.key, None) is not None:
            del tokens[self.key]
        return True

    def GetTokens(self):
        net: Net = NetCore.Get(self.net_name)
        tokens = net.tokens
        return tokens

    def GetToken(self, key):
        net: Net = NetCore.Get(self.net_name)
        tokens = net.tokens
        return tokens.get(key, None)

    @abstractmethod
    def SendClientResponse(self, response: ClientResponseModel):
        pass

    @abstractmethod
    def SendServerRequest(self, request: ServerRequestModel):
        pass

    def OnLog(self, log: TrackLog = None, code=None, message=None):
        if log is None:
            log = TrackLog(code=code, message=message)
        log.server = self
        self.log_event.OnEvent(log=log)

    def OnException(self, exception: TrackException = None, code=None, message=None):
        if exception is None:
            exception = TrackException(code=code, message=message)
        exception.server = self
        self.exception_event.OnEvent(exception=exception)
