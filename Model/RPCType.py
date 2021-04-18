import json

from Model.RPCException import RPCException, ErrorCode


def deserialize(cls, _json):
    instance = cls()
    di = json.loads(_json)
    try:
        instance.__dict__ = di
    except:
        instance = di
    return instance


class RPCType:

    def __init__(self):
        self.abstractType = dict()
        self.abstractName = dict()
        self.typeConvert = dict()

    def add(self, **kwargs):
        _type = kwargs.get("type", None)
        type_name = kwargs.get("type_name", None)
        convert = kwargs.get("convert", deserialize)
        self.detect(_type, type_name)
        self.abstractName[_type.__name__] = type_name
        self.typeConvert[type_name] = convert
        self.abstractType[type_name] = _type

    def detect(self, _type, type_name):
        if self.typeConvert.get(type_name, None) is not None:
            raise RPCException(ErrorCode.RegisterError, "转换器中已包含" + type_name)
        if self.abstractType.get(type_name, None) is not None:
            raise RPCException(ErrorCode.RegisterError, "真实类中已包含" + type_name)
        if self.abstractName.get(_type, None) is not None:
            raise RPCException(ErrorCode.RegisterError, "抽象类中已包含" + type_name)
