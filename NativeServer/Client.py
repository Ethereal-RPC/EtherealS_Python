# client.py
# -*-coding:utf-8
import json
from twisted.internet import protocol, reactor
from Model.ClientResponseModel import ClientResponseModel
from Utils import JsonTool

HOST = 'localhost'  # 要连接的IP地址
PORT = 9295  # 端口


class TSClntProtocol(protocol.Protocol):  # 同服务端一样
    def sendData(self, data):  # 定义一个发送数据的方法
        if data:
            request = ClientResponseModel()
            child = ClientResponseModel()
            child.Service = "SSSS"
            request.init("2.0", "result", "result_type", "22", "service", child)
            di = json.dumps(request, cls=JsonTool.JSONEncoder)
            print(di)
            self.transport.write(json.dumps(di).encode())  # 发送数据
        else:
            self.transport.loseConnection()  # 当没有输入时断开连接

    def connectionMade(self):
        self.sendData("asd".encode())  # 调用方法

    def dataReceived(self, data):
        print(data)
        self.sendData()


class TSClntFactory(protocol.ClientFactory):  # 我的理解是客户端写protocol.ClientFactory，服务端写protocol.SocketListener
    protocol = TSClntProtocol  # 同服务端一样


clientConnectionLost = clientConnectionFailed = lambda self, connector, reason: reactor.stop()

reactor.connectTCP(HOST, PORT, TSClntFactory())  # 跟服务端一样
reactor.run()

