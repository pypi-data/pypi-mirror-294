# coding: utf8
import os
import sys
from pathlib import Path


def path_not_exist(path: str | Path) -> bool:
    """
    判断目标路径是否存在
    如果参数为空或者 None，亦认为不存在

    :param path: 目标路径
    :return:
    """
    if isinstance(path, str):
        return len(path) == 0 or not Path(path).exists()
    elif isinstance(path, Path):
        return not path.exists()
    else:
        return True


def path_exists(path: str | Path) -> bool:
    """
    对 path_not_exist 的相反包装

    :param path: 目标路径
    :return:
    """
    return not path_not_exist(path)


def get_log_dir() -> str | None:
    if sys.platform == "win32":
        log_dir = Path(os.path.expanduser("~"), "AppData", "Roaming")
    elif sys.platform == "darwin":
        log_dir = Path(os.path.expanduser("~"),  "Library", "Application Support")
    else:
        return None
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    return str(log_dir)
