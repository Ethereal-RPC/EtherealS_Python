from abc import abstractmethod

from EtherealS.Extension.Authority.IAuthoritable import IAuthoritable


class IAuthorityCheck(IAuthoritable):
    @abstractmethod
    def check(self, authoritable):
        pass
