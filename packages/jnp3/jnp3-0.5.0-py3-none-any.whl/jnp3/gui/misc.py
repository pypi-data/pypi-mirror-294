# coding: utf8
from ._compat import (
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
