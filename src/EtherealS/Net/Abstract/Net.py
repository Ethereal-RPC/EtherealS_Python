from abc import ABC, abstractmethod
from enum import Enum

from EtherealS.Core.BaseCore.BaseCore import BaseCore
from EtherealS.Server.Abstract import Server
from EtherealS.Net.Abstract.NetConfig import NetConfig
from EtherealS.Service.Abstract.Service import Service


class NetType(Enum):
    WebSocket = 1


class Net(ABC,BaseCore):
    def __init__(self, name, config):
        BaseCore.__init__(self)
        self.tokens = dict()
        self.name = name
        self.server: Server = None
        self.config: NetConfig = config
        self.services = dict()
        self.interceptorEvent = list()
        self.type = None

    @abstractmethod
    def Publish(self):
        pass

    def OnInterceptor(self, service: Service, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(self, service, method, token):
                return False
        return True
