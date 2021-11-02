from numbers import Number

from EtherealS.Service.Decorator import ServiceMethod
from EtherealS.Service.WebSocket.WebSocketService import WebSocketService
from EtherealS_Test.User import User


class UserService(WebSocketService):
    def Initialize(self):
        pass

    def UnInitialize(self):
        pass

    def __init__(self, name, types):
        super().__init__()
        self.request = None
        self.name = name
        self.types = types
        self.userRequest = None

    @ServiceMethod.ServiceMethod()
    def Register(self, user: User, username: str, id: Number) -> bool:
        user.username = username
        user.id = id
        return user.Register()

    @ServiceMethod.ServiceMethod()
    def SendSay(self, sender: User, listener_id: Number, message: str) -> bool:
        listener = sender.GetToken(listener_id)
        if listener is not None:
            self.userRequest.Say(listener, sender, message)
            return True
        else:
            return False

    @ServiceMethod.ServiceMethod()
    def Add(self, sender: User, a: int, b: int) -> int:
        from EtherealS.Request import RequestCore
        from EtherealS_Test.UserRequest import UserRequest
        request: UserRequest = RequestCore.Get(net_name="demo", service_name="Client")
        sender.username = "M"
        request.Say(sender, sender, "你好呀")
        return a + b
