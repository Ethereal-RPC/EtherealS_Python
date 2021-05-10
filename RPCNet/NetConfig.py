from Model.BaseUserToken import BaseUserToken
from RPCService.Service import Service


class NetConfig:

    def __init__(self):
        self.interceptorEvent = list()

    def OnInterceptor(self, service: Service, method, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(service, method, token):
                return False
        return True
