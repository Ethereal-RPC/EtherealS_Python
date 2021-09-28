from EtherealC.Service.WebSocket.WebSocketService import WebSocketService

class ClientNodeService(WebSocketService):
    def __init__(self):
        self.serverNodeRequest = None
