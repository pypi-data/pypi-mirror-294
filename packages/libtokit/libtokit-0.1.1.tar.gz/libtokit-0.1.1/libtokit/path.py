import os
from typing import Tuple


def mkdirs(path: str, exist_ok: bool = True) -> Tuple[bool, str]:
    """
    创建指定路径的目录。

    :param path: 需要创建的目录路径
    :param exist_ok: 如果目录已存在是否忽略错误，默认为True
    :return: err, msg
    """
    try:
        os.makedirs(path, exist_ok=exist_ok)
        return False, "ok"
    except Exception as e:
        return True, f"{e}"
