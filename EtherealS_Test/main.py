from numbers import Number

from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Net.WebSocket.WebSocketNet import WebSocketNet
from EtherealS.Server.WebSocket.WebSocketServer import WebSocketServer
from EtherealS_Test.User import User
from EtherealS_Test.UserRequest import UserRequest
from EtherealS_Test.UserService import UserService
from EtherealS.Server import ServerCore
from EtherealS.Net import NetCore
from EtherealS.Request import RequestCore
from EtherealS.Service import ServiceCore


def OnException(exception: TrackException):
    print(exception.exception)


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
    prefixes = list()
    prefixes.append("ethereal://127.0.0.1:28015/NetDemo/".replace("28015", port))
    print("Server-{0}".format(prefixes))
    # 建立网关
    net = NetCore.Register(WebSocketNet("demo"))
    net.exception_event.Register(OnException )
    net.log_event.Register(OnLog )
    # 注册服务
    service = ServiceCore.Register(net=net, service=UserService())
    # 注册请求
    request = RequestCore.Register(request=UserRequest(), service=service)
    # 突出Service为正常类
    service.userRequest = request
    # 注册连接
    server = ServerCore.Register(net=net, server=WebSocketServer(prefixes))
    net.Publish()
    print("服务器初始化完成....")


if __name__ == '__main__':
    Single()


