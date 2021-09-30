from EtherealS.Request.Decorator import Request
from EtherealS.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealS_Test.User import User


class UserRequest(WebSocketRequest):
    def __init__(self, name, types):
        WebSocketRequest.__init__(self, name, types)
    
    @Request.Request()
    def Say(self, user: User, sender: User, message: str) -> None:
        pass
