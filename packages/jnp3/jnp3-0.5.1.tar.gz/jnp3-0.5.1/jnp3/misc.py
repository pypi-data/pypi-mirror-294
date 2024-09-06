# coding: utf8
import sys
import inspect
import warnings
from logging import Logger
from types import TracebackType
from typing import Type


class FakeLogger(object):
    """当没有提供 Logger 时占位用的"""

    def debug(self, msg: str):
        pass

    def info(self, msg: str):
        pass

    def warning(self, msg: str):
        pass

    def error(self, msg: str):
        pass

    def critical(self, msg: str):
        pass


def get_excepthook_for(logger: Logger):

    def my_excepthook(
            exc_type: Type[BaseException],
            exc_value: BaseException,
            exc_traceback: TracebackType | None,
    ):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("Found exception", exc_info=(exc_type, exc_value, exc_traceback))

    return my_excepthook


def deprecated(reason):
    """参考自 openpyxl/compat/__init__.py"""
    if isinstance(reason, (bytes, str)):
        def outer(func):
            if inspect.isclass(func):
                msg = "Call to deprecated class `{name}`. ({reason})"
            else:
                msg = "Call to deprecated function `{name}`. ({reason})"

            def inner(*args, **kwargs):
                warnings.warn(message=msg.format(name=func.__name__, reason=reason),
                              category=DeprecationWarning, stacklevel=2)
                return func(*args, **kwargs)

            return inner
        return outer

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        obj = reason
        if inspect.isclass(obj):
            info = "Call to deprecated class {name}."
        else:
            info = "Call to deprecated function {name}."

        def deco(*args, **kwargs):
            warnings.warn(message=info.format(name=obj.__name__),
                          category=DeprecationWarning, stacklevel=2)
            return obj(*args, **kwargs)

        return deco

    else:
        raise TypeError("Unsupported usage")


def url2cn(url: str, encoding='utf8'):
    """将url中的编码转换成中文"""
    template = "b'{url}'"
    return eval(template.format(url=url.replace('%', '\\x'))).decode(encoding)


def group_by(items: list, size: int) -> list[tuple]:
    """
    group_by([1, 2, 3, 4, 5, 6], 3) -> [(1, 2, 3), (4, 5, 6)]

    :param items: 元素列表
    :param size: 每组的元素个数
    :return: 所有分组的列表
    """
    if len(items) % size != 0:
        raise ValueError("Cannot be evenly grouped")
    return list(zip(*[iter(items)] * size))
