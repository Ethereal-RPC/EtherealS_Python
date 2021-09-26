from Server.WebSocket.WebSocketBaseToken import WebSocketBaseToken


class User(WebSocketBaseToken):
    def __init__(self):
        super(WebSocketBaseToken, self).__init__()
        self.id = None
        self.username = None

    def serialize(self):
        json = dict()
        json["ID"] = self.id
        json["UserName"] = self.username
        return json
