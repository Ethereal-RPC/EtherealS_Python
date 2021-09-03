from Model.BaseUserToken import BaseUserToken
from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from Model.RPCTypeConfig import RPCTypeConfig
from RPCService import Service
from Utils.Event import Event


class ServiceConfig:

    def __init__(self, _type: RPCTypeConfig):
        self.types: RPCTypeConfig = _type
        self.interceptorEvent = list()
        self.authoritable = False

    def OnInterceptor(self, service: Service, method: classmethod, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            item: method
            if not item.__call__(service, method, token):
                return False
        return True
