import sys
from twisted.internet.defer import log

from EtherealS_Test.UserRequest import UserRequest
from EtherealS_Test.UserService import UserService
from Model.BaseUserToken import BaseUserToken
from Model.RPCTypeConfig import RPCTypeConfig
from NativeServer import ServerCore
from NativeServer.ServerConfig import ServerConfig
from RPCNet import NetCore
from RPCNet.NetConfig import NetConfig
from RPCRequest import RequestCore
from RPCService import ServiceCore
from Utils.Event import Event


def create_method(**kwargs):
    print(kwargs.get("p1"))
    print(kwargs.get("p2"))
    print(kwargs.get("p3"))


if __name__ == '__main__':
    create_method(p1=2, p2=3)
