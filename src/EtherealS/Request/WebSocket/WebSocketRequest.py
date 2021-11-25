from abc import ABC

from EtherealS.Request.Abstract.Request import Request
from EtherealS.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


class WebSocketRequest(Request, ABC):

    def __init__(self):
        super().__init__()
        self.config = WebSocketRequestConfig()
