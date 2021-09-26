from Core.Model.AbstractTypes import AbstractTypes
from Net.Abstract.Net import Net


class WebSocketNet(Net):
    def __init__(self, net_name):
        super().__init__(net_name=net_name)

    def Publish(self):
        if self.config.netNodeMode:
            types: AbstractTypes = AbstractTypes()

        self.server.Start()
        return True
