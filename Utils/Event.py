class Event:
    def __init__(self):
        self.__listeners__ = list()

    def register(self, delegate):
        self.__listeners__.append(delegate)

    def unregister(self, delegate):
        self.__listeners__.remove(delegate)

    def onEvent(self, **params):
        for delegate in self.__listeners__:
            delegate(**params)
