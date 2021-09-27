import EtherealC.Service.ServiceCore

from EtherealS.Net.Abstract.Net import Net


class WebSocketNet(Net):
    def __init__(self, net_name):
        super().__init__(net_name=net_name)

    def Publish(self):
        if self.config.netNodeMode:
            # 服务端
            from EtherealS.Core.Model.AbstractTypes import AbstractTypes
            from EtherealS.Net.NetNode.Model.NetNode import NetNode
            from EtherealS.Net.NetNode.NetNodeServer.Service.ServerNodeService import ServerNodeService
            from EtherealS.Net.NetNode.NetNodeServer.Request.ClientNodeRequest import ClientNodeRequest
            from EtherealS.Service import ServiceCore
            from EtherealS.Request import RequestCore
            types: AbstractTypes = AbstractTypes()
            types.add(type=int, type_name="Int")
            types.add(type=str, type_name="String")
            types.add(type=bool, type_name="Bool")
            types.add(type=type(NetNode()), type_name="NetNode")
            ServiceCore.Register(net=self, instance=ServerNodeService(), service_name="ServerNetNodeService",
                                 types=types)
            RequestCore.Register(net=self, instance=ClientNodeRequest(), service_name="ClientNetNodeService",
                                 types=types)

            # 客户端
            from EtherealC.Core.Model.AbstractTypes import AbstractTypes
            from EtherealC.Service import ServiceCore
            from EtherealC.Request import RequestCore
            from EtherealC.Net import NetCore
            from EtherealC.Net.Abstract.Net import NetType
            from EtherealS.Net.NetNode.NetNodeClient.Service.ClientNodeService import ClientNodeService
            from EtherealS.Net.NetNode.NetNodeClient.Request.ServerNodeRequest import ServerNodeRequest
            for item in self.config.netNodeIps:
                prefixes = item[0]
                config = item[1]
                types: AbstractTypes = AbstractTypes()
                types.add(type=int, type_name="Int")
                types.add(type=str, type_name="String")
                types.add(type=bool, type_name="Bool")
                types.add(type=type(NetNode()), type_name="NetNode")
                net = NetCore.Register(net_name="NetNodeClient-{0}".format(prefixes), type=NetType.WebSocket)
                net.config.netNodeMode = False
                clientNodeService: ClientNodeService = EtherealC.Service.ServiceCore.Register(net=net,
                                                                                              service_name="ClientNetNodeService",
                                                                                              types=types,
                                                                                              instance=ClientNodeService())
                clientNodeService.serverNodeRequest = EtherealC.Request.RequestCore.Register(net=net,
                                                                                             service_name="ServerNetNodeService",
                                                                                             types=types,
                                                                                             instance=ServerNodeRequest())
                net.log_event.register(self.OnLog)
                net.exception_event.register(self.OnException)

        self.server.Start()
        return True
