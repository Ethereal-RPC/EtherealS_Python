from Decorator import RPCService
from Model.BaseUserToken import BaseUserToken


class UserService:

    @RPCService.RPCService()
    def Hello(self, token: BaseUserToken, s: str) -> str:
        return s + "你好！"
