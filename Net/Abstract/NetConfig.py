from abc import ABC

from Service.Abstract.Service import Service


class NetConfig(ABC):

    def __init__(self):
        self.interceptorEvent = list()
        self.netNodeMode = False
        self.netNodeIps = None
        self.netNodeHeartbeatCycle = 60000

    def OnInterceptor(self, service: Service, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(service, method, token):
                return False
        return True
