from abc import abstractmethod
from typing import List, Type

from .sites import SiteBase
from service.session import AsyncSession


class Parser:

    @abstractmethod
    def create_parser(self) -> SiteBase:
        """"""

    async def get_proxy_data(self, session: Type[AsyncSession]) -> List[str]:
        parser = self.create_parser()
        data = await parser.parse_data(session)
        result = [str(proxy) for proxy in data]
        return result

