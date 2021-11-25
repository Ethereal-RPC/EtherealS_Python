from EtherealS.Core.Model.TrackException import TrackException, ExceptionCode

nets = dict()


def Get(name):
    return nets.get(name)


def Register(net):
    if not net.isRegister:
        net.isRegister = True
        nets[net.name] = net
    else:
        raise TrackException(code=ExceptionCode.Core, message="Net:{0}已注册".format(net.name))
    return nets[net.name]


def UnRegister(net):
    if net.isRegister:
        if nets.__contains__(net.name):
            del nets[net.name]
        net.isRegister = False
        return True
    else:
        raise TrackException(ExceptionCode.Core, "{0}已经UnRegister".format(net.name))
