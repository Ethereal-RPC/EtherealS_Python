from Decorator import RPCRequest
from EtherealS_Test.User import User
from Model.BaseUserToken import BaseUserToken


class UserRequest:
    @RPCRequest.RPCRequest()
    def Say(self, user: User, sender: User, message: str) -> None:
        pass
