from Decorator import RPCRequest
from Model.BaseUserToken import BaseUserToken


class UserRequest:
    @RPCRequest.RPCRequest()
    def Hello(self, token: BaseUserToken, name: str) -> None:
        pass
