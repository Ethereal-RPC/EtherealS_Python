from numbers import Number

from EtherealS.Request.Decorator import RequestMapping
from EtherealS.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealS_Test.User import User


class UserRequest(WebSocketRequest):
    def Register(self):
        pass

    def UnRegister(self):
        pass

    def UnInitialize(self):
        pass

    def Initialize(self):
        self.name = "Client"
        self.types.add(type=int, type_name="Int")
        self.types.add(type=type(User()), type_name="User")
        self.types.add(type=Number, type_name="Number")
        self.types.add(type=str, type_name="String")
        self.types.add(type=bool, type_name="Bool")
    
    @RequestMapping.RequestMapping("Say")
    def Say(self, token: User, sender: User, message: str) -> None:
        pass
