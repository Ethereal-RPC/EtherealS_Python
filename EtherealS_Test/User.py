from NativeServer.BaseToken import BaseToken


class User(BaseToken):
    def __init__(self):
        BaseToken.__init__(self)
        self.id = None
        self.username = None
