import asyncio
from typing import List, Tuple

from service.session import AsyncSession


class ProxyChecker:

    def __init__(self, proxies: List[bytes], url: str, timeout: int):
        self.proxies = proxies
        self.check_url = url
        self.max_timeout = timeout

    async def check_ip(self, ip: bytes) -> Tuple[bool, bytes]:
        try:
            status, _ = await AsyncSession.get(self.check_url,
                                               proxy="http://" + ip.decode(),
                                               timeout=self.max_timeout)
        except Exception as exc:
            print(f"{ip.decode()}: {repr(exc)}")  # TODO replace print to logging
            return False, ip
        return True, ip

    async def get_failed_proxies(self):
        tasks = [self.check_ip(ip) for ip in self.proxies]
        for result in asyncio.as_completed(tasks):
            is_working, address = await result
            if not is_working:
                yield address

