from numbers import Number

from Service.Decorator import Service
from EtherealS_Test.User import User


class UserService:
    def __init__(self):
        self.userRequest = None

    @Service.RPCService()
    def Register(self, user: User, username: str, id: Number) -> bool:
        user.username = username
        user.id = id
        return user.Register()

    @Service.RPCService()
    def SendSay(self, sender: User, listener_id: Number, message: str) -> bool:
        listener = sender.GetToken(listener_id)
        if listener is not None:
            self.userRequest.Say(listener, sender, message)
            return True
        else:
            return False

    @Service.RPCService()
    def Add(self, a: int, b: int) -> int:
        return a + b
