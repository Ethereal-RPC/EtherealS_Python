import sys
from twisted.internet.defer import log

from EtherealS_Test.UserRequest import UserRequest
from EtherealS_Test.UserService import UserService
from Model.BaseUserToken import BaseUserToken
from Model.RPCType import RPCType
from NativeServer import ServerCore
from NativeServer.ServerConfig import ServerConfig
from RPCNet import NetCore
from RPCNet.NetConfig import NetConfig
from RPCRequest import RequestCore
from RPCService import ServiceCore


def create_method():
    return BaseUserToken()


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = "28014"
    rType = RPCType()
    rType.add(type=str, type_name="String")
    NetCore.RegisterByConfig(ip, port, NetConfig())
    ServiceCore.RegisterByType(UserService(), ip, port, "ServerService", rType)
    server = ServerCore.RegisterByMethod(ip, port, create_method)
    server.run()
    # 配置将日志输出到stdout
    log.startLogging(sys.stdout)
