from EtherealS.Core.Model.AbstractTypes import AbstractTypes
from EtherealS.Service.Abstract import Service
from EtherealS.Service.Abstract.ServiceConfig import ServiceConfig


class WebSocketServiceConfig(ServiceConfig):

    def __init__(self, _type: AbstractTypes):
        super().__init__(_type)
