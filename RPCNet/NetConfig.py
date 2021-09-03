from Model.BaseUserToken import BaseUserToken
from Model.RPCException import RPCException
from Model.RPCLog import RPCLog
from RPCService.Service import Service
from Utils.Event import Event


class NetConfig:

    def __init__(self):
        self.interceptorEvent = list()
        self.netNodeMode = False
        self.netNodeIps = None
        self.netNodeHeartbeatCycle = 60000

    def OnInterceptor(self, service: Service, method, token: BaseUserToken) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(service, method, token):
                return False
        return True


