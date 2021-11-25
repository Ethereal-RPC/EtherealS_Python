from EtherealS.Core.Manager.Event.Decorator.Event import Event
from EtherealS.Core.Manager.Event.Model.EventContext import EventContext


class EventClass:
    def __init__(self):
        self.name = "Event"

    @Event(mapping="after")
    def Test(self,s:str,d:int,event_context: EventContext):
        print(self.name)
        print(s)
        print(d)
        print(event_context)
