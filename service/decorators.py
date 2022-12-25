import asyncio
import functools
from datetime import timedelta, datetime

from .exceptions import TaskIsNotCoroutine


def task(fn=None, interval: float = None, eta: timedelta = None,
         verbose: bool = False):

    def wrapper(coro):
        if not asyncio.iscoroutinefunction(coro):
            raise TaskIsNotCoroutine("Wrapped task should be coroutine.")

        @functools.wraps(coro)
        async def wrapped(*args, **kwargs):
            if eta:
                await asyncio.sleep(eta.total_seconds())
            while True:
                res = await coro(*args, **kwargs)
                log = f"[{datetime.now()}] Task {coro.__name__} was completed."
                if verbose:
                    log += f" Task result: {res}."
                print(log)
                if not interval:
                    break
                await asyncio.sleep(interval)

        wrapped.is_task = True
        return wrapped
    return wrapper(fn) if fn else wrapper
