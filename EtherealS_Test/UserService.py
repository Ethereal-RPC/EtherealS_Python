from numbers import Number

from EtherealS.Core.Manager.Event.Decorator.AfterEvent import AfterEvent
from EtherealS.Service.Decorator import ServiceMapping
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

    @ServiceMapping.ServiceMapping("Add")
    def Add(self, token: User, a: int, b: int) -> int:
        from EtherealS.Request import RequestCore
        from EtherealS_Test.UserRequest import UserRequest
        request: UserRequest = RequestCore.Get(net_name="demo", service_name="Client")
        token.username = "M"
        request.Say(token, token, "你好呀")
        return a + b

    @ServiceMapping.ServiceMapping("test")
    @AfterEvent(method="instance.after(s:s,d:d)")
    def Test(self, token: User, s: str, d: int, k: int) -> bool:
        print("Test")
        return True
