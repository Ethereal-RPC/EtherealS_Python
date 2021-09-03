import sys
from numbers import Number
from EtherealS_Test.User import User
from EtherealS_Test.UserService import UserService
from Model.RPCTypeConfig import RPCTypeConfig
from NativeServer import ServerCore
from RPCNet import NetCore
from RPCRequest import RequestCore
from RPCService import ServiceCore
import sys
import os


def OnException(**kwargs):
    exception = kwargs.get("exception")
    print(exception)


def OnLog(**kwargs):
    exception = kwargs.get("log")
    print(exception)


def CreateMethod():
    return User()


if __name__ == '__main__':
    ip = "127.0.0.1"
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
    print("Server-{0}-{1}".format(ip, port))
    types = RPCTypeConfig()
    types.add(type=int, type_name="Int")
    types.add(type=type(User()), type_name="User")
    types.add(type=Number, type_name="Number")
    types.add(type=str, type_name="String")
    types.add(type=bool, type_name="Bool")
    # 建立网关
    net = NetCore.Register(name="demo")
    net.exception_event.Register(OnException)
    net.log_event.Register(OnLog)
    # 注册服务
    service = ServiceCore.Register(instance=UserService(), net=net, service_name="Server", type_config=types)
    # 注册请求
    request = RequestCore.Register(net=net, service_name="Client", type_config=types)
    # 突出Service为正常类
    service.instance.userRequest = request
    # 注册连接
    server = ServerCore.Register(net=net, ip=ip, port=port, create_method=CreateMethod)
    ips = list()
    # 分布式这里需要引用客户端框架，但是目前Python还没有客户端版本，暂且搁置.
    # EtherealC.NativeClient.ClientConfig clientConfig = new EtherealC.NativeClient.ClientConfig();
    net.config.netNodeMode = False
    config = None
    ips.append(dict(ip=ip, port="28015", config=config))
    ips.append(dict(ip=ip, port="28016", config=config))
    ips.append(dict(ip=ip, port="28017", config=config))
    ips.append(dict(ip=ip, port="28018", config=config))
    ips.append(dict(ip=ip, port="28019", config=config))
    net.config.netNodeIps = ips
    net.Publish()
    print("服务器初始化完成....")
