from abc import ABC
from types import MethodType
from EtherealS.Service.Abstract.Service import Service
from EtherealS.Service.WebSocket.WebSocketToken import WebSocketToken
from EtherealS.Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


class WebSocketService(Service, ABC):
    def __init__(self):
        super().__init__()
        self.config = WebSocketServiceConfig()

        def create():
            return WebSocketToken()

        self.create_method = create
