from Model.BaseUserToken import BaseUserToken
from Model.RPCType import RPCType
from RPCService.Service import Service


class ServiceConfig:
    interceptorEvent = list()
    tokenEnable = None
    type: RPCType = None
    authoritable = None

    def __init__(self, type):
        self.type = type

    def OnInterceptor(self, service: Service, method: classmethod, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            item: method
            if not item.__call__(service, method, token):
                return False
        return True
