import asyncio
import random
import re
from base64 import b64decode
from typing import List, Type

import numpy as np
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

from settings.dev import settings
from .base import SiteBase
from service.parsers.ip_data import ProxyIP
from service.session import AsyncSession
from service.parsers.sites.exceptions import StatusCodeError
from ..exceptions import InvalidIPAddress


class FreeProxyCz(SiteBase):
    base_url: str = "http://free-proxy.cz/en/proxylist/main/date/1"
    timeouts: np.ndarray = np.arange(1, 4, 0.2)

    @staticmethod
    def parse_ip_data(row: List[Tag]) -> ProxyIP:
        ip_js = row[0].script.text
        ip_b64 = re.search("(\.decode\(.)(.+)(.\)\))", ip_js).group(2)
        ip = b64decode(ip_b64).decode()
        obj = ProxyIP(ip=ip, port=row[1].text)
        return obj

    @staticmethod
    def _get_next_btn(soup: Tag) -> Tag:
        paginator = soup.find("div", {"class": "paginator"})
        next_btn = paginator.find("a", string="Next »")
        return next_btn

    def _parse_table(self, table: Tag) -> List[ProxyIP]:
        rows = table.find_all("tr")[1:]
        res = []
        for row in rows:
            if row.find("td", {"colspan": "11"}):
                continue
            col_vals = row.find_all("td")
            try:
                ip_data = self.parse_ip_data(col_vals)
                res.append(ip_data)
            except InvalidIPAddress as err:
                print(err)  # TODO replace print to logging
        return res

    async def _parse_data(self, url: str,
                          sess: Type[AsyncSession]) -> List[ProxyIP]:
        result = []
        try:
            html_content = await self._send_request(url, sess)
            soup = BeautifulSoup(html_content, settings.bs_parser)
            table = soup.find(id="proxy_list")
            next_btn = self._get_next_btn(soup)
            if not (table and next_btn):
                return result
            result += self._parse_table(table)
            next_page = int(next_btn["href"].split("/")[-1])
            new_url = urljoin(url[:-1], str(next_page))
            await asyncio.sleep(random.choice(self.timeouts))
            result += await self._parse_data(new_url, sess)
        except StatusCodeError as err:
            print(err)  # TODO replace print to logging

        return result

    async def parse_data(self, sess: Type[AsyncSession]) -> List[ProxyIP]:
        res = await self._parse_data(self.base_url, sess)
        return res
