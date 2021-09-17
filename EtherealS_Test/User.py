from Server.WebSocket.WebSocketBaseToken import WebSocketBaseToken


class User(WebSocketBaseToken):
    def __init__(self):
        super().__init__()
        self.id = None
        self.username = None
