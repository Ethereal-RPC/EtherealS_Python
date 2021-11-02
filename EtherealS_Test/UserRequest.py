from EtherealS.Request.Decorator import RequestMethod
from EtherealS.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealS_Test.User import User


class UserRequest(WebSocketRequest):
    def UnInitialize(self):
        pass

    def Initialize(self):
        pass

    def __init__(self, name, types):
        super().__init__()
        self.name = name
        self.types = types
    
    @RequestMethod.RequestMethod()
    def Say(self, user: User, sender: User, message: str) -> None:
        pass
