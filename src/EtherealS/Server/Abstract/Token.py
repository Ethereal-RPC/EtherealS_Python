from abc import ABC, abstractmethod

from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Core.Model.TrackLog import TrackLog
from EtherealS.Core.Model import ServerRequestModel
from EtherealS.Net import NetCore
from EtherealS.Core.Event import Event


class Token(ABC):
    def __init__(self):
        super().__init__()
        self.key = None
        self.config = None
        self.net = None
        self.exception_event = Event()
        self.log_event = Event()
        self.connect_event = Event()
        self.disconnect_event = Event()

    def Register(self, replace=False):
        from EtherealS.Net.Abstract.Net import Net
        net: Net = NetCore.Get(self.net_name)
        tokens = net.tokens
        if tokens is not None:
            if replace is False:
                if tokens.get(self.key, None) is not None:
                    return True
            tokens[self.key] = self
            return True

    def UnRegister(self):
        from EtherealS.Net.Abstract.Net import Net
        net: Net = NetCore.Get(self.net_name)
        tokens = net.tokens
        if tokens.get(self.key, None) is not None:
            del tokens[self.key]
        return True

    def GetTokens(self):
        from EtherealS.Net.Abstract.Net import Net
        net: Net = NetCore.Get(self.net_name)
        tokens = net.tokens
        return tokens

    def GetToken(self, key):
        from EtherealS.Net.Abstract.Net import Net
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

    @abstractmethod
    def serialize(self):
        pass
