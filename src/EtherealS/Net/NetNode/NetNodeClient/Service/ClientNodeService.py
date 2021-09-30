from EtherealC.Service.WebSocket.WebSocketService import WebSocketService


class ClientNodeService(WebSocketService):
    def __init__(self,name,types):
        super().__init__(name,types)
