import logging
from datetime import timedelta

import aioredis

from .decorators import task
from service.session import AsyncSession
from service.parsers import FreeProxyListParser, FreeProxyCzParser
from service.proxy_checker import ProxyChecker
from service.main import redis_pool
from settings.dev import settings


logger = logging.getLogger(__name__)


@task(interval=settings.parse_interval,
      eta=timedelta(seconds=10))
async def parse_freeproxylist():
    redis = aioredis.Redis(connection_pool=redis_pool)
    parser = FreeProxyListParser()
    proxies_list = await parser.get_proxy_data(AsyncSession)
    await redis.lpush(settings.redis_proxy_key, *proxies_list)
    print(f"push {len(proxies_list)} proxies to redis")  # TODO replace to logging


@task(interval=settings.parse_interval,
      eta=timedelta(seconds=20))
async def parse_freeproxycz():
    redis = aioredis.Redis(connection_pool=redis_pool)
    parser = FreeProxyCzParser()
    proxies_list = await parser.get_proxy_data(AsyncSession)
    await redis.lpush(settings.redis_proxy_key, *proxies_list)
    print(f"push {len(proxies_list)} proxies to redis")  # TODO replace to logging


@task(interval=settings.check_interval)
async def check_proxies():
    redis = aioredis.Redis(connection_pool=redis_pool)
    proxies = await redis.lrange(settings.redis_proxy_key, 0, -1)
    checker = ProxyChecker(proxies, settings.check_url,
                           timeout=settings.checker_timeout)
    async for proxy in checker.get_failed_proxies():
        await redis.lrem(settings.redis_proxy_key, 0, proxy)
    
