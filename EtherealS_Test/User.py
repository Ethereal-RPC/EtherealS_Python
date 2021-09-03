from Model.BaseUserToken import BaseUserToken


class User(BaseUserToken):
    def __init__(self):
        BaseUserToken.__init__(self)
        self.id = None
        self.username = None