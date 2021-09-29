from EtherealC.Request.Decorator.Request import Request
from EtherealC.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealS.Net.NetNode.Model.NetNode import NetNode


class ServerNodeRequest(WebSocketRequest):
    @Request()
    def Register(self, node: NetNode) -> bool:
        pass
