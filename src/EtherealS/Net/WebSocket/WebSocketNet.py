from EtherealS.Net.Abstract.Net import Net
from EtherealS.Net.WebSocket.WebSocketNetConfig import WebSocketNetConfig


class WebSocketNet(Net):
    def __init__(self, name):
        super().__init__(name=name, config=WebSocketNetConfig())
        import threading
        self.connectSign = threading.Event()

    def Publish(self):
        def reactorStart():
            from twisted.internet import reactor
            if not reactor.running:
                reactor.suggestThreadPoolSize(10)
                reactor.run(False)

        import threading
        threading.Thread(target=reactorStart).start()
        self.server.Start()
        return True

