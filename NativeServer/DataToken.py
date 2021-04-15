import json
import sys
from datetime import time
from random import Random
from typing import Tuple

from twisted.internet.protocol import ServerFactory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor

from Model.BaseUserToken import BaseUserToken
from RPCService.ServiceConfig import ServiceConfig
from Utils import JsonTool


class DataToken(Protocol):
    # BaseUserToken
    token: BaseUserToken
    # 组包
    __content: bytearray = bytearray(1024)
    __needRemain = 0
    # 头包
    __head_size = 32
    __body_size = 4
    __pattern_size = 1
    __future_size = 27
    # 用于接收数据
    __pattern = 0
    __future = bytearray(__future_size)

    config: ServiceConfig
    serverKey: (str, str)

    def __init__(self, server_key, config: ServiceConfig):
        self.config = config
        self.serverKey = server_key

    # 连接成功事件，可重载
    def connectionMade(self):
        self.token.connect_event()
        log.msg("Client connection from %s" % self.client_ip)

    # 连接断开事件，可重载，依靠reason区分断开类型
    def connectonLost(self, reason):
        self.token.disconnect_event()
        log.msg('Lost client connection. Reason: %s' % reason)

    def dataReceived(self, data):
        writer_index = data.__len__()
        reader_index = 0
        while reader_index < writer_index:
            if self.__needRemain != 0:
                if self.__needRemain <= writer_index - reader_index:

