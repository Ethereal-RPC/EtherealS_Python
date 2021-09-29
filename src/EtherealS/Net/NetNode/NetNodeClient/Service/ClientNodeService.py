from EtherealC.Service.WebSocket.WebSocketService import WebSocketService

class ClientNodeService(WebSocketService):
    def __init__(self):
        super(ClientNodeService, self).__init__()
        self.serverNodeRequest = None
