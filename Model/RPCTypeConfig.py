import json

from Model.RPCException import RPCException, ExceptionCode
from Model.RPCType import RPCType
from Utils import JsonTool


class RPCTypeConfig:

    def __init__(self):
        self.typesByType = dict()
        self.typesByName = dict()

    def add(self, **kwargs):
        rpc_type = RPCType()
        rpc_type.type = kwargs.get("type", None)
        rpc_type.name = kwargs.get("type_name", None)

        def deserializeFunc(_json):
            instance = rpc_type.type()
            di = None
            try:
                di = json.loads(_json)
            except:
                di = _json
            try:
                instance.__dict__ = di
            except:
                instance = di
            return instance

        def serializeFunc(obj):
            return json.dumps(obj, cls=JsonTool.JSONEncoder)

        rpc_type.deserialize = deserializeFunc
        rpc_type.serialize = serializeFunc
        self.detect(rpc_type.type, rpc_type.name)
        self.typesByName[rpc_type.name] = rpc_type
        self.typesByType[rpc_type.type] = rpc_type

    def detect(self, _type, type_name):
        if self.typesByName.get(type_name, None) is not None:
            raise RPCException(ExceptionCode.Core, "真实类中已包含" + type_name)
        if self.typesByType.get(_type, None) is not None:
            raise RPCException(ExceptionCode.Core, "抽象类中已包含" + type_name)
