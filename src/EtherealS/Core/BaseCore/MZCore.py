from EtherealS.Core.BaseCore.BaseCore import BaseCore
from EtherealS.Core.Event import Event
from EtherealS.Core.Manager.AbstractType.AbstractTypeManager import AbstractTypeManager
from EtherealS.Core.Manager.Ioc.IocManager import IocManager
from EtherealS.Core.Model.TrackException import TrackException
from EtherealS.Core.Model.TrackLog import TrackLog


class MZCore(BaseCore):
    def __init__(self):
        BaseCore.__init__(self)
        self.iocManager = IocManager()
        self.types = AbstractTypeManager()
