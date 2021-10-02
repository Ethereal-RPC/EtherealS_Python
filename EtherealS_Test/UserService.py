from numbers import Number

from EtherealS.Service.Decorator import Service
from EtherealS.Service.WebSocket.WebSocketService import WebSocketService
from EtherealS_Test.User import User


class UserService(WebSocketService):
    def __init__(self, name, types):
        super().__init__()
        self.request = None
        self.name = name
        self.types = types
        self.userRequest = None

    @Service.Service()
    def Register(self, user: User, username: str, id: Number) -> bool:
        user.username = username
        user.id = id
        return user.Register()

    @Service.Service()
    def SendSay(self, sender: User, listener_id: Number, message: str) -> bool:
        listener = sender.GetToken(listener_id)
        if listener is not None:
            self.userRequest.Say(listener, sender, message)
            return True
        else:
            return False

    @Service.Service()
    def Add(self, sender: User, a: int, b: int) -> int:
        from EtherealS.Request import RequestCore
        from EtherealS_Test.UserRequest import UserRequest
        request: UserRequest = RequestCore.Get(net_name="demo", service_name="Client")
        sender.username = "M"
        request.Say(sender, sender, "你好呀")
        return a + b
