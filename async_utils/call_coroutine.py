import asyncio
from typing import List
from typing import Coroutine

def call_coroutines(coros: List[Coroutine]):
    """
    用于在同步函数中调用异步函数

    Args:
        funcs (List[Coroutine]): 要运行的异步函数集

    """
    loop = asyncio.get_event_loop()

    tasks = [loop.create_task(coro) for coro in coros]

    if loop.is_running():
        asyncio.gather(*tasks, return_exceptions=True)
    else:
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
