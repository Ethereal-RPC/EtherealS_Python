from numbers import Number

from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Net.WebSocket.WebSocketNet import WebSocketNet
from EtherealS.Server.WebSocket.WebSocketServer import WebSocketServer
from EtherealS_Test.User import User
from EtherealS_Test.UserRequest import UserRequest
from EtherealS_Test.UserService import UserService
from EtherealS.Core.Model.AbstractTypes import AbstractTypes
from EtherealS.Net.Abstract.Net import NetType
from EtherealS.Server import ServerCore
from EtherealS.Net import NetCore
from EtherealS.Request import RequestCore
from EtherealS.Service import ServiceCore


def OnException(exception: TrackException):
    print(exception)


def OnLog(**kwargs):
    from EtherealS.Core.Model.TrackLog import TrackLog
    log: TrackLog = kwargs.get("log")
    print(log.message)


def CreateMethod():
    return User()


def Single():
    port = "28015"
    print("请选择端口(0-3)")
    mode = input()
    if mode == "0":
        port = "28015"
    elif mode == "1":
        port = "28016"
    elif mode == "2":
        port = "28017"
    elif mode == "3":
        port = "28018"
    else:
        port = mode
    prefixes = "ethereal://127.0.0.1:28015/NetDemo/".replace("28015", port)
    print("Server-{0}".format(prefixes))
    types = AbstractTypes()
    types.add(type=int, type_name="Int")
    types.add(type=type(User()), type_name="User")
    types.add(type=Number, type_name="Number")
    types.add(type=str, type_name="String")
    types.add(type=bool, type_name="Bool")
    # 建立网关
    net = NetCore.Register(WebSocketNet("demo"))
    net.exception_event.Register(OnException)
    net.log_event.Register(OnLog)
    # 注册服务
    service = ServiceCore.Register(net=net, service=UserService("Server", types))
    # 注册请求
    request = RequestCore.Register(net=net, request=UserRequest("Server", types))
    # 突出Service为正常类
    service.userRequest = request
    # 注册连接
    server = ServerCore.Register(net=net, server=WebSocketServer(prefixes, CreateMethod))
    ips = list()
    net.Publish()
    print("服务器初始化完成....")


def NetNode():
    port = "28015"
    print("请选择端口(0-3)")
    mode = input()
    if mode == "0":
        port = "28015"
    elif mode == "1":
        port = "28016"
    elif mode == "2":
        port = "28017"
    elif mode == "3":
        port = "28018"
    else:
        port = mode
    prefixes = "ethereal://127.0.0.1:28015/NetDemo/".replace("28015", port)
    print("Server-{0}".format(prefixes))
    types = AbstractTypes()
    types.add(type=int, type_name="Int")
    types.add(type=type(User()), type_name="User")
    types.add(type=Number, type_name="Number")
    types.add(type=str, type_name="String")
    types.add(type=bool, type_name="Bool")
    # 建立网关
    net = NetCore.Register(WebSocketNet("demo"))
    net.exception_event.Register(OnException)
    net.log_event.Register(OnLog)
    # 注册服务
    service = ServiceCore.Register(net=net, service=UserService("Server", types))
    # 注册请求
    request = RequestCore.Register(net=net, request=UserRequest("Server", types))
    # 突出Service为正常类
    service.userRequest = request
    # 注册连接
    server = ServerCore.Register(net=net,server=WebSocketServer(prefixes,CreateMethod))
    ips = list()
    net.config.netNodeMode = True
    ips.append(dict(prefixes="ethereal://127.0.0.1:28015/NetDemo/".replace("28015", "28015"), config=None))
    ips.append(dict(prefixes="ethereal://127.0.0.1:28015/NetDemo/".replace("28015", "28016"), config=None))
    ips.append(dict(prefixes="ethereal://127.0.0.1:28015/NetDemo/".replace("28015", "28017"), config=None))
    ips.append(dict(prefixes="ethereal://127.0.0.1:28015/NetDemo/".replace("28015", "28018"), config=None))
    net.config.netNodeIps = ips
    net.Publish()
    print("服务器初始化完成....")


if __name__ == '__main__':
    # Single()
    NetNode()


