import json
from typing import Any

from Core.Model.ClientResponseModel import ClientResponseModel
from Core.Model.Error import Error


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        from Server.Abstract.BaseToken import BaseToken
        if isinstance(obj, BaseToken):
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
