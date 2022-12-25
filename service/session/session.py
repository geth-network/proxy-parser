from typing import Tuple

from aiohttp import ClientSession, TCPConnector

from service.session.exceptions import NotFoundSession


class AsyncSession:

    _sess: ClientSession = None

    @classmethod
    def init_session(cls, **kwargs):
        if not cls._sess:
            cls._sess = ClientSession(connector=TCPConnector(),
                                      **kwargs)

    @classmethod
    async def disconnect(cls):
        if cls._sess:
            await cls._sess.close()

    @classmethod
    async def get(cls, url: str, **kwargs) -> Tuple[int, str]:
        if not cls._sess:
            raise NotFoundSession("AIOHTTP Session is None")
        async with cls._sess.get(url, **kwargs) as resp:
            content = await resp.text()
        return resp.status, content

    @classmethod
    async def post(cls, url: str, payload: dict, **kwargs) -> Tuple[str, int]:
        if not cls._sess:
            raise NotFoundSession("AIOHTTP Session is None")
        async with cls._sess.post(url, json=payload, **kwargs) as resp:
            content = await resp.text()
        return content, resp.status

