import json
from twisted.internet.protocol import Protocol
from twisted.python import log

from EtherealS_Test.UserRequest import UserRequest
from Model.BaseUserToken import BaseUserToken
from Model.ClientRequestModel import ClientRequestModel
from Model.RPCException import RPCException
from Model.RPCType import RPCType
from NativeServer.ServerConfig import ServerConfig
from RPCNet import NetCore

# 头包
from RPCRequest import RequestCore

head_size = 32
body_size = 4
pattern_size = 1
future_size = 27


class DataToken(Protocol):

    def __init__(self, server_key, config: ServerConfig):
        self.config = config
        self.serverKey = server_key
        # BaseUserToken
        self.token: BaseUserToken = None
        # 组包
        self.content: bytearray = None

    # 连接成功事件，可重载
    def connectionMade(self):
        self.token = self.config.create_method.__call__()
        self.token.net = self.transport
        if self.token.connect_event.__len__() > 0:
            self.token.connect_event()
        print("Client connection from {0}".format(self.serverKey))

    # 连接断开事件，可重载，依靠reason区分断开类型
    def connectonLost(self, reason):
        if self.token.disconnect_event.__len__() > 0:
            self.token.disconnect_event()
        log.msg('Lost client connection. Reason: %s' % reason)

    def dataReceived(self, data):
        write_index = data.__len__()
        reader_index = 0
        count = write_index
        # 缓冲区有数据
        if self.content is not None:
            # 数据区头包还没凑齐
            if self.content.__len__() < head_size:
                head_need = body_size - self.content.__len__()
                if count >= head_need:
                    self.content.extend(data[reader_index:head_need])
                    reader_index += head_need
                    count -= head_need
                else:
                    self.content.extend(data[reader_index::])
                    return
            # 解析头包
            body_length = int.from_bytes(data[reader_index:reader_index + body_size:], byteorder='little')
            pattern = data[reader_index + body_size:reader_index + body_size:]
            future: bytes = data[reader_index + body_size + pattern_size:reader_index + head_size:]
            length = body_length + head_size
            if body_length > self.config.buffer_size:
                self.connectonLost("超出上限")
                raise RPCException(RPCException.ErrorCode.RuntimeError, "{0}-{1}:{2}用户请求数据量太大,中止接收！"
                                   .format(self.serverKey, self.transport.getPeer().host,
                                           self.transport.getPeer().port))
            # 判断数据是否能够完全缓冲
            if length != self.content.__len__() and length < self.content.__len__() + count:
                # 从读idx到读idx + 还缺x个数据
                self.content.extend(data[reader_index:reader_index + length - self.content.__len__():])
                reader_index += length - self.content.__len__()
                count -= length - self.content.__len__()
            else:
                self.content.extend(data[reader_index::])
                return
            di = json.loads(self.content.decode(self.config.encode))
            request = ClientRequestModel()
            request.__dict__ = di
            net_config = NetCore.Get(self.serverKey)
            if net_config is None:
                raise RPCException(RPCException.ErrorCode.RuntimeError,
                                   "{0}找不到NetConfig".format(self.serverKey))
            if pattern == 0:
                net_config.clientRequestReceive(self.serverKey, self.token, request)
                self.content = None
        # Content内没有了数据,开始尝试直接读取缓冲区数据,之所以这样写，是减少数据copy次数，能够一次性读取的就一次性读取并释放
        while reader_index < write_index:
            # 数据已经无法判断头包了
            if count < head_size:
                self.content = bytearray(data[reader_index::])
                return
            # 解析头包
            body_length = int.from_bytes(data[reader_index:reader_index + body_size:], byteorder='little')
            pattern = data[reader_index + body_size]
            future: bytes = data[reader_index + body_size + pattern_size:reader_index + head_size:]
            length = body_length + head_size
            if body_length > self.config.buffer_size:
                self.connectonLost("超出上限")
                raise RPCException(RPCException.ErrorCode.RuntimeError, "{0}-{1}:{2}用户请求数据量太大,中止接收！"
                                   .format(self.serverKey, self.transport.getPeer().host,
                                           self.transport.getPeer().port))
            # 判断数据能否直接解析
            if length > count:
                # 数据不够用，放入content
                self.content = bytearray(data[reader_index::])
                return
            # 数据够用
            di = json.loads(data[reader_index + head_size:reader_index + length].decode(self.config.encode))
            request = ClientRequestModel()
            request.__dict__ = di
            net_config = NetCore.Get(self.serverKey)
            if net_config is None:
                raise RPCException(RPCException.ErrorCode.RuntimeError,
                                   "{0}找不到NetConfig".format(self.serverKey))
            if pattern == 0:
                net_config.clientRequestReceive(self.serverKey, self.token, request)
            reader_index += length