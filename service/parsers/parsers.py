from .base import Parser
from .sites import SiteBase, FreeProxyList, FreeProxyCz


class FreeProxyListParser(Parser):

    def create_parser(self) -> SiteBase:
        return FreeProxyList()


class FreeProxyCzParser(Parser):

    def create_parser(self) -> SiteBase:
        return FreeProxyCz()
