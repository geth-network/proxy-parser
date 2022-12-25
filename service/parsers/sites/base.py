from abc import abstractmethod
from typing import List, Type

from bs4 import Tag

from service.parsers.ip_data import ProxyIP
from service.parsers.sites.exceptions import StatusCodeError
from service.session import AsyncSession


class SiteBase:

    @property
    @abstractmethod
    def base_url(self):
        """"""

    @staticmethod
    @abstractmethod
    def parse_ip_data(row: List[Tag]) -> ProxyIP:
        """"""

    @abstractmethod
    async def parse_data(self, sess: Type[AsyncSession]) -> List[ProxyIP]:
        """"""

    @staticmethod
    async def _send_request(url: str, sess: Type[AsyncSession]) -> str:
        status, content = await sess.get(url)
        if status >= 400:
            raise StatusCodeError(f"{url} - status code: {status}")
        return content
