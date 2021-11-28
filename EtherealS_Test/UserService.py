from numbers import Number

from EtherealS.Core.Manager.Event.Decorator.AfterEvent import AfterEvent
from EtherealS.Service.Decorator.ServiceMapping import ServiceMapping
from EtherealS.Service.WebSocket.WebSocketService import WebSocketService
from EtherealS_Test.EventClass import EventClass
from EtherealS_Test.User import User


class UserService(WebSocketService):
    def Initialize(self):
        self.name = "Server"
        self.types.add(type=int, type_name="Int")
        self.types.add(type=type(User()), type_name="User")
        self.types.add(type=Number, type_name="Number")
        self.types.add(type=str, type_name="String")
        self.types.add(type=bool, type_name="Bool")
        self.iocManager.Register("instance", EventClass())

    def Register(self):
        pass

    def UnRegister(self):
        pass

    def UnInitialize(self):
        pass

    @ServiceMapping("Add")
    def Add(self, a: int, b: int) -> int:
        return a + b

    @ServiceMapping("Login")
    def Login(self, token: User,username: str) -> bool:
        token.username = username
        return True

    @ServiceMapping("Hello")
    def Hello(self, token: User) -> str:
        return "Hello,{0}.".format(token.username)








    @ServiceMapping("test")
    @AfterEvent(method="instance.after(s:s,d:d)")
    def Test(self, token: User, s: str, d: int, k: int) -> bool:
        print("Test")
        return True
