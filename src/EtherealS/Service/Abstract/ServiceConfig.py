from abc import ABC

from EtherealS.Core.Model.AbstractTypes import AbstractTypes
from EtherealS.Service.Abstract import Service


class ServiceConfig(ABC):

    def __init__(self, _type: AbstractTypes):
        self.types: AbstractTypes = _type
        self.interceptorEvent = list()
        self.authoritable = False

    def OnInterceptor(self, service: Service, method: classmethod, token) -> bool:
        for item in self.interceptorEvent:
            item: method
            if not item.__call__(service, method, token):
                return False
        return True
