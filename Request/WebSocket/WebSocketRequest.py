from types import MethodType

from Core.Model.TrackException import TrackException
from Request.Abstract.Request import Request
from Request.Decorator.Request import RequestAnnotation
from Core.Model import TrackLog
from Core.Model.AbstractType import AbstrackType
from Core.Model import ServerRequestModel
from Request.Abstract.RequestConfig import RequestConfig
from Core.Event import Event


class WebSocketRequest(Request):

    def __init__(self, config: RequestConfig):
        super().__init__(config)
