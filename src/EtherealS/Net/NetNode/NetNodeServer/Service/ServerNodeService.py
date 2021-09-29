import random

from EtherealS.Net.NetNode.Model.NetNode import NetNode

from EtherealS.Server.Abstract.BaseToken import BaseToken
from EtherealS.Service.Decorator.Service import Service
from EtherealS.Service.WebSocket.WebSocketService import WebSocketService


class ServerNodeService(WebSocketService):
    def __init__(self):
        super(ServerNodeService, self).__init__()
        self.netNodes = dict()
        self.random = random.Random()

    @Service()
    def Register(self, token: BaseToken, node: NetNode) -> bool:
        token.key = "{0}-{1}".format(node.Name, node.Prefixes)
        value = self.netNodes.get(token.key, None)
        if value is not None:
            old_token: BaseToken = value[0]
            old_token.disconnect_event.UnRegister(self.Sender_DisConnectEvent)
        self.netNodes[token.key] = (token, node)
        token.disconnect_event.Register(self.Sender_DisConnectEvent)
        print("{0}注册节点成功".format(token.key))
        self.printNetNodes()
        return True

    @Service()
    def GetNetNode(self,token: BaseToken, service_name: str) -> NetNode:
        nodes = list()
        for item in self.netNodes.values():
            node: NetNode = item[1]
            if node.Services.get(service_name, None) is not None:
                nodes.append(node)
        if nodes.__len__() > 0:
            return nodes[self.random.randint(0, nodes.__len__())]
        return None

    def Sender_DisConnectEvent(self,token):
        del self.netNodes[token.key]
        print("成功删除节点")
        self.printNetNodes()

    def printNetNodes(self):
        sb = "当前信息节点：\n"
        for item in self.netNodes.values():
            sb += item[0].key + "\n"
        print(sb)
