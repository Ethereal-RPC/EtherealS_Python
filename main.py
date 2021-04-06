from types import MethodType

from Decorator.RPCService import RPCService, ServiceAnnotation
from Model.BaseUserToken import BaseUserToken
from RPCService.Service import Service


def say1(something):
    """
        123
        sss
    """
    print("say" + something)


def Request(timeout):
    def wrap(f):
        f.__doc__ = say1.__doc__

        def func(*args, **kwargs):

            return f(*args, **kwargs)
        func.__doc__ = timeout
        return func

    return wrap


class UserToken(BaseUserToken):
    a = None


def say(something: bool, sd: int):
    print("执行了")


if __name__ == '__main__':
    service = Service
    if issubclass(say.__annotations__["something"], int):
        print(list(say.__annotations__.values()))


