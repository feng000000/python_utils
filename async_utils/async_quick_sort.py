from typing import Any
from typing import List
from typing import Callable
from typing import Coroutine
from .task_group_python310 import TaskGroup

async def async_sort(
    data: List,
    key: Callable[[Any], Coroutine],
    reverse: bool = False,
) -> List:
    """
    异步版本快速排序

    Args:
        data (List): 待排序列表
        key (Callable[[Any], Coroutine]): 异步获取data中元素的值
        reverse (bool): 默认为 False, 从小到大排

    example key func:
    ```python
        async def key(x):
            return await get_name(x)
    ```

    Returns:
        List: 返回排序好的列表

    """
    task_group = TaskGroup()
    for item in data:
        task_group.append(key(item))
    data_value = await task_group.get()

    def cmp(x, y):
        if reverse:
            return x > y
        return x < y

    async def quick_sort(left: int, right: int):
        nonlocal key
        nonlocal data
        nonlocal data_value

        if left >= right:
            return

        # 使data左边都小于mid_value, 右边都大于mid_value
        idx = (left + right) // 2
        mid_value = data_value[idx]
        i = left - 1
        j = right + 1
        while i < j:
            i += 1
            while cmp(data_value[i], mid_value):
                i += 1

            j -= 1
            while cmp(mid_value, data_value[j]):
                j -= 1

            if i < j:
                data[i], data[j] = data[j], data[i]
                data_value[i], data_value[j] = data_value[j], data_value[i]

        # 递归处理左右两边的子区间
        await quick_sort(left, j)
        await quick_sort(j + 1, right)


    await quick_sort(0, len(data) - 1)
    return data
