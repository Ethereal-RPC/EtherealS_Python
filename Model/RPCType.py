import json

from Model.RPCException import RPCException, ErrorCode


def deserialize(_json):
    return json.loads(_json)


class RPCType:
    abstractName = dict
    abstractType = dict
    typeConvert = dict

    def add(self, _type, type_name):
        self.detect(_type, type_name)
        self.AbstractName[_type] = type_name
        self.TypeConvert[type_name] = deserialize
        self.AbstractType[type_name] = _type

    def add(self, _type, type_name, convert):
        self.detect(_type, type_name)
        self.AbstractName[_type] = type_name
        self.TypeConvert[type_name] = convert
        self.AbstractType[type_name] = _type

    def detect(self, _type, type_name):
        if self.TypeConvert.get(type_name, None) is not None:
            raise RPCException(ErrorCode.RegisterError, "转换器中已包含" + type_name)
        if self.AbstractType.get(type_name, None) is not None:
            raise RPCException(ErrorCode.RegisterError, "真实类中已包含" + type_name)
        if self.AbstractName.get(_type, None) is not None:
            raise RPCException(ErrorCode.RegisterError, "抽象类中已包含" + type_name)
