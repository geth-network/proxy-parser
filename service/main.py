import asyncio

import aioredis
from fake_http_header import FakeHttpHeader

from service.tools import collect_tasks
from service.session import AsyncSession
from settings.dev import settings


redis_pool = aioredis.ConnectionPool.from_url(settings.redis_url)


async def main():
    headers = FakeHttpHeader(domain_name="pl").as_header_dict()
    AsyncSession.init_session(headers=headers)
    tasks = collect_tasks()
    await asyncio.gather(*tasks)

    await AsyncSession.disconnect()
    await redis_pool.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
