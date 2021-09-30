import EtherealC.Service.ServiceCore

from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealS.Net.Abstract.Net import Net


class WebSocketNet(Net):
    def __init__(self, net_name):
        super().__init__(net_name=net_name)
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
            from EtherealC.Client import ClientCore
            from EtherealC.Client.Abstract import Client
            from EtherealS.Net.NetNode.NetNodeClient.Service.ClientNodeService import ClientNodeService
            from EtherealS.Net.NetNode.NetNodeClient.Request.ServerNodeRequest import ServerNodeRequest
            from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode
            for item in self.config.netNodeIps:
                prefixes = item["prefixes"]
                config = item["config"]
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
                                                                                              config=config,
                                                                                              instance=ClientNodeService())
                clientNodeService.serverNodeRequest = EtherealC.Request.RequestCore.Register(net=net,
                                                                                             service_name="ServerNetNodeService",
                                                                                             types=types,
                                                                                             config=config,
                                                                                             instance=ServerNodeRequest())
                net.log_event.register(self.OnLog)
                net.exception_event.register(self.OnException)
            import threading

            def NetNodeSearchRunner():
                from EtherealS.Net import NetCore as ServerNetCore
                while ServerNetCore.Get(self.net_name) is not None:
                    try:
                        for tuple in self.config.netNodeIps:
                            prefixes = tuple["prefixes"]
                            clientConfig = tuple["config"]
                            net = NetCore.Get("NetNodeClient-{0}".format(prefixes))
                            if net is None:
                                raise TrackException(code=ExceptionCode.Runtime,
                                                     message="未找到Net：NetNodeClient-{0}".format(prefixes))
                            request = EtherealC.Request.RequestCore.Get(net=net,
                                                                        service_name="ServerNetNodeService")
                            if request is None:
                                raise TrackException(code=ExceptionCode.Runtime,
                                                     message="未找到Request：{0}-{1}".format(net.net_name,
                                                                                         "ServerNetNodeService"))
                            if request.client is not None:
                                continue

                            client: Client = ClientCore.Register(net=net, request=request, prefixes=prefixes,
                                                                 config=clientConfig)
                            client.connectSuccess_event.register(self.ClientNodeConnectSuccess)
                            client.connectFail_event.register(self.ClientNodeConnectFail)
                            client.disconnect_event.register(self.ClientNodeDisConnect)
                            net.Publish()
                    except Exception as e:
                        self.OnException(TrackException(code=ExceptionCode.Runtime, message=e.args, exception=e))
                    finally:
                        self.connectSign.wait(self.config.netNodeHeartbeatCycle / 1000)
                        self.connectSign.clear()

            threading.Thread(target=NetNodeSearchRunner).start()
        self.server.Start()
        return True

    def ClientNodeConnectSuccess(self, client):
        from EtherealC.Request import RequestCore
        from EtherealS.Net.NetNode.NetNodeClient.Request.ServerNodeRequest import ServerNodeRequest
        serverNodeRequest: ServerNodeRequest = RequestCore.Get(net_name="NetNodeClient-{0}".format(client.prefixes),
                                                                service_name="ServerNetNodeService")
        if serverNodeRequest is not None:
            from EtherealS.Net.NetNode.Model.NetNode import NetNode
            node = NetNode()
            node.Prefixes.append(self.server.prefixes)
            node.Name = self.net_name
            for service in self.services.values():
                from EtherealS.Net.NetNode.Model.ServiceNode import ServiceNode
                serviceNode = ServiceNode()
                serviceNode.name = service.service_name
                node.Services[serviceNode.name] = serviceNode
            for request in self.requests.values():
                from EtherealS.Net.NetNode.Model.RequestNode import RequestNode
                requestNode = RequestNode()
                requestNode.name = request.service_name
                node.Requests[requestNode.name] = requestNode
            serverNodeRequest.Register(node)
        else:
            raise TrackException(code=ExceptionCode.Runtime,
                                 message="EtherealC中未找到 NetNodeClient-{0}-ServerNodeService".format(client.prefixes))

    def ClientNodeConnectFail(self, client):
        from EtherealC.Client import ClientCore
        ClientCore.UnRegister(net_name=client.net_name,service_name=client.service_name)

    def ClientNodeDisConnect(self, client):
        from EtherealC.Client import ClientCore
        self.connectSign.set()
        ClientCore.UnRegister(net_name=client.net_name,service_name=client.service_name)


