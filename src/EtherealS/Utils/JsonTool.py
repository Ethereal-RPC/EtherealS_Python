import json
from typing import Any

from EtherealS.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealS.Core.Model.Error import Error


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        from EtherealS.Service.Abstract.Token import Token
        if isinstance(obj, Token):
            return obj.serialize()
        else:
            d = {}
            d.update(obj.__dict__)
            return d


class JSONClientResponseModel(json.JSONEncoder):
    def default(self, obj: ClientResponseModel) -> Any:
        if isinstance(obj, Error):
            obj.Code = obj.Code.name
            return obj.__dict__
