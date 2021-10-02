from EtherealS.Request.Decorator import Request
from EtherealS.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealS_Test.User import User


class UserRequest(WebSocketRequest):
    def __init__(self, name, types):
        super().__init__()
        self.name = name
        self.types = types
    
    @Request.Request()
    def Say(self, user: User, sender: User, message: str) -> None:
        pass
