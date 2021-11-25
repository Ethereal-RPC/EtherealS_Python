from EtherealS.Service.WebSocket.WebSocketToken import WebSocketToken


class User(WebSocketToken):
    def __init__(self):
        super(WebSocketToken, self).__init__()
        self.id = -1
        self.username = None

    def serialize(self):
        json = dict()
        json["ID"] = self.id
        json["UserName"] = self.username
        return json
