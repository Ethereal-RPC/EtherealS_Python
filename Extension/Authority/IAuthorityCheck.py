from abc import abstractmethod

from Extension.Authority.IAuthoritable import IAuthoritable


class IAuthorityCheck(IAuthoritable):
    @abstractmethod
    def check(self, authoritable):
        pass
