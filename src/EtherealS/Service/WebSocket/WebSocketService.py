from types import MethodType
from EtherealS.Service.Abstract.Service import Service
from EtherealS.Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


class WebSocketService(Service):
    def __init__(self, name, types):
        super().__init__(name, types)
        self.config = WebSocketServiceConfig()
