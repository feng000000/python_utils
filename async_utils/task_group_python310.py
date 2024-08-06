import asyncio
from asyncio import Task
from typing import Any
from typing import List
from typing import Coroutine

class TaskGroup:
    def __init__(
        self, coros: List[Coroutine] = [], batch_size: int = -1
    ) -> None:
        """
        TaskGroup 用于并行执行任务, 使用 `get()` 或 `get_noexcept()` 获取执行结果

        Usage
        ```python
            task_group = TaskGroup(coros = [
                async_func1("xxx")
                async_func2("xxx")
            ])
            task_group.append(async_func2("xxx"))
            res: List = await task_group.get()
        ```

        Args:
            coros (List[Awaitable], optional): 任务列表. Defaults to [].
            batch_size: 并行执行的最大任务数, 如果 `len(coros) > batch_size` 会分批次执行.
                `-1` 代表不限制

        """
        self._batch_size = batch_size
        self._coro_group: List[Coroutine] = []
        for coro in coros:
            self._coro_group.append(coro)

    def append(self, coro: Coroutine) -> None:
        """
        向Group中添加一个异步任务

        Args:
            func (Awaitable):

        """
        self._coro_group.append(coro)

    async def _create_tasks(self, coros: List[Coroutine]) -> List[Task]:
        """
        通过 asyncio.create_task 创建 Task

        """
        tasks: List[Task] = []
        for coro in coros:
            task = asyncio.create_task(coro)
            tasks.append(task)
        return tasks

    async def _shedule_tasks(self, tasks: List[Task]) -> List:
        """
        异步执行 tasks

        """
        res_list = []
        for task in tasks:
            res_list.append(await task)
        return res_list

    async def _shedule_tasks_noexcept(self, tasks: List[Task]) -> List:
        """
        异常安全地异步执行 tasks, 如果发生异常返回值则为对应的 Exception

        """
        res_list = []
        for task in tasks:
            try:
                res_list.append(await task)
            except Exception as e:
                res_list.append(e)
        return res_list

    async def get(self) -> List[Any]:
        """
        异步执行任务, 任务全部完成时, 返回结果列表.
        任务发生异常时直接抛出

        Returns:
            List[Any]: 函数执行的结果集

        """
        res_list = []

        if self._batch_size == -1:
            tasks = await self._create_tasks(self._coro_group)
            return await self._shedule_tasks(tasks)

        curren_num = 0
        while curren_num < len(self._coro_group):
            start = curren_num
            end = curren_num + self._batch_size

            tasks = await self._create_tasks(self._coro_group[start:end])
            res = await self._shedule_tasks(tasks)
            res_list.extend(res)

            curren_num = end

        return res_list

    async def get_noexpect(self) -> List[Any]:
        """
        异步执行任务, 任务全部完成时, 返回结果列表.
        该函数不会抛出异常,
        任务发生异常时, 返回列表中对应任务的值为抛出的异常

        Returns:
            List[Any]: 函数执行的结果集

        """
        res_list = []

        if self._batch_size == -1:
            tasks = await self._create_tasks(self._coro_group)
            return await self._shedule_tasks_noexcept(tasks)

        curren_num = 0
        while curren_num < len(self._coro_group):
            start = curren_num
            end = curren_num + self._batch_size

            tasks = await self._create_tasks(self._coro_group[start:end])
            res = await self._shedule_tasks_noexcept(tasks)
            res_list.extend(res)

            curren_num = end

        return res_list
