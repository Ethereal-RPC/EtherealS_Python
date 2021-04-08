from Model.BaseUserToken import BaseUserToken
from RPCService import ServiceCore
from RPCService.Service import Service


class NetConfig:
    __tokens = dict()
    interceptorEvent = list()
    baseUserToken_instance_method = None
    clientRequestReceive = ServiceCore.ClientRequestReceive
    serverRequestSend = None
    clientResponseSend = None

    def OnInterceptor(self, service: Service, method, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(service, method, token):
                return False
        return True

    def __init__(self, instance_method: staticmethod):
        self.baseUserToken_instance_method = instance_method
