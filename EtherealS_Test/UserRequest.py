from EtherealS.Request.Decorator import Request
from EtherealS.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealS_Test.User import User


class UserRequest(WebSocketRequest):
    @Request.Request()
    def Say(self, user: User, sender: User, message: str) -> None:
        pass
