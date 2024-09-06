# coding: utf8
from typing import Callable
from ._compat import (
    QObject,
    QMessageBox, QWidget,
)


def accept_warning(widget: QWidget, condition: bool,
                   caption: str = "Warning", text: str = "Are you sure to continue?") -> bool:
    if condition:
        b = QMessageBox.question(widget, caption, text)
        if b == QMessageBox.StandardButton.No:
            return True
    return False


def argb32_to_rgb(argb32: int):
    return argb32 & 0x00FFFFFF


def get_exec(obj: QObject) -> Callable:
    if hasattr(obj, "exec"):
        return obj.exec
    elif hasattr(obj, "exec_"):
        return obj.exec_
    else:
        raise AttributeError
