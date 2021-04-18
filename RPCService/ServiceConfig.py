from Model.BaseUserToken import BaseUserToken
from Model.RPCType import RPCType
from RPCService import Service


class ServiceConfig:

    def __init__(self, _type):
        self.type = _type
        self.interceptorEvent = list()
        self.tokenEnable = True
        self.authoritable = False

    def OnInterceptor(self, service: Service, method: classmethod, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            item: method
            if not item.__call__(service, method, token):
                return False
        return True
