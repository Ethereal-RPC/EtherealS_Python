from Request.Decorator import Request
from EtherealS_Test.User import User


class UserRequest:
    @Request.RPCRequest()
    def Say(self, user: User, sender: User, message: str) -> None:
        pass
