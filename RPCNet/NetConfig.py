from Model.BaseUserToken import BaseUserToken
from RPCService.Service import Service


class NetConfig:

    def __init__(self):
        self.tokens = dict()
        self.interceptorEvent = list()
        self.clientRequestReceive = None
        self.serverRequestSend = None
        self.clientResponseSend = None

    def OnInterceptor(self, service: Service, method, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(service, method, token):
                return False
        return True
