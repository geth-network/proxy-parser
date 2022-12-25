from typing import List, Type

from bs4 import BeautifulSoup, Tag

from .base import SiteBase
from service.parsers.ip_data import ProxyIP
from service.session import AsyncSession
from service.parsers.sites.exceptions import StatusCodeError


class FreeProxyList(SiteBase):
    base_url = "https://free-proxy-list.net/"
    table_selector = 'table:-soup-contains("IP Address")'

    @staticmethod
    def parse_ip_data(row: List[Tag]) -> ProxyIP:
        obj = ProxyIP(ip=row[0].text, port=row[1].text)
        return obj

    async def parse_data(self, sess: Type[AsyncSession]) -> List[ProxyIP]:
        res = []
        try:
            html_content = await self._send_request(self.base_url, sess)
            soup = BeautifulSoup(html_content, "lxml")
            table = soup.select_one(self.table_selector)
            rows = table.find_all("tr")[1:]

            for row in rows:
                col_vals = row.find_all("td")
                ip_data = self.parse_ip_data(col_vals)
                res.append(ip_data)
        except StatusCodeError as err:
            print(err)  # TODO replace print to logging
        return res
