# coding: utf8
from .._compat import (
    QSize, Signal,
    QIcon,
    QPushButton, QWidget,
)
from ..icon import get_icon_from_svg


class PushButtonWithItem(QPushButton):

    clicked_with_item = Signal(object)

    def __init__(self, item: object, title: str = "", parent: QWidget = None):
        super().__init__(title, parent)
        self.item = item
        self.clicked.connect(self.on_self_clicked)

    def on_self_clicked(self):
        self.clicked_with_item.emit(self.item)


class IconPushButton(QPushButton):

    def __init__(
            self,
            svg_icon: str | QIcon,
            w: int = None,
            h: int = None,
            parent: QWidget = None
    ):
        super().__init__(parent)

        if isinstance(svg_icon, str):
            icon = get_icon_from_svg(svg_icon, w, h)
        elif isinstance(svg_icon, QIcon):
            icon = svg_icon
        else:
            raise ValueError("svg_icon must be str or QIcon instance")

        self.setIcon(icon)
        if w is not None and h is not None:
            self.setIconSize(QSize(w, h))
