from EtherealS.Core.Manager.Event.Decorator.EventSender import EventSender


class TimeoutEvent(EventSender):
    def __init__(self,method):
        EventSender.__init__(self,method)
        self.isThrow = False

    def __call__(self, func):
        func.ethereal_timeoutEvent = self
        EventSender.__call__(self,func)
        return func