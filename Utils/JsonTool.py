import json

from Model.ClientResponseModel import ClientResponseModel


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d


class JSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict2obj)

    def dict2obj(self, d):
        instance = ClientResponseModel()
        instance.__dict__ = d
        return instance