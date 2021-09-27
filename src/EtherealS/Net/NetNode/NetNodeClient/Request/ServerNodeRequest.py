from EtherealS.Net.NetNodeClient.Model.NetNode import NetNode
from EtherealS.Request.Decorator.Request import Request


class ServerNodeRequest:
    @Request()
    def Register(self, node: NetNode):
        pass
