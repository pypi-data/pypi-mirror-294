# coding: utf8
from .._compat import (
    Signal,
    QIcon,
    QGroupBox, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget,
)
from .lines import HorizontalLine
from .buttons import PushButtonWithItem
from ..icon import get_icon_from_svg


# 图标来自 https://freeicons.io/profile/3
red_close_svg = """
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 60.963 60.842" style="enable-background:new 0 0 60.963 60.842;" xml:space="preserve">
<path style="fill: rgb(247, 5, 17);" d="M59.595,52.861L37.094,30.359L59.473,7.98c1.825-1.826,1.825-4.786,0-6.611
c-1.826-1.825-4.785-1.825-6.611,0L30.483,23.748L8.105,1.369c-1.826-1.825-4.785-1.825-6.611,0c-1.826,1.826-1.826,4.786,0,6.611
l22.378,22.379L1.369,52.861c-1.826,1.826-1.826,4.785,0,6.611c0.913,0.913,2.109,1.369,3.306,1.369s2.393-0.456,3.306-1.369
l22.502-22.502l22.501,22.502c0.913,0.913,2.109,1.369,3.306,1.369s2.393-0.456,3.306-1.369
C61.42,57.647,61.42,54.687,59.595,52.861z" id="id_101"></path>
</svg>
"""


class Card(QGroupBox):

    def __init__(self, title: str = "", icon: QIcon = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.icon = icon

        self.vly_m = QVBoxLayout()
        self.setLayout(self.vly_m)
        self.hly_top = QHBoxLayout()
        self.vly_m.addLayout(self.hly_top)

        self.lb_icon = QLabel(self)
        self.lb_title = QLabel(self.title, self)
        self.pbn_close = PushButtonWithItem(self, "", self)
        self.pbn_close.setFixedWidth(25)
        self.pbn_close.setFlat(True)
        self.pbn_close.setIcon(get_icon_from_svg(red_close_svg, 32, 32))

        self.hly_top.addWidget(self.lb_icon)
        self.hly_top.addWidget(self.lb_title)
        self.hly_top.addStretch(1)
        self.hly_top.addWidget(self.pbn_close)

        self.hln_1 = HorizontalLine(self)
        self.vly_m.addWidget(self.hln_1)

        self.cw = QLabel("Nothing here...", self)
        self.vly_m.addWidget(self.cw)

        if self.icon is not None:
            self.set_icon(self.icon)

    def set_central_widget(self, widget: QWidget):
        self.vly_m.removeWidget(self.cw)
        self.cw.deleteLater()

        self.cw = widget
        self.vly_m.addWidget(self.cw)

    def set_title(self, title: str):
        self.title = title
        self.lb_title.setText(title)

    def set_icon(self, icon: QIcon):
        self.icon = icon
        self.lb_icon.setText("")
        self.lb_icon.setPixmap(icon.pixmap(20, 20))


class CardsArea(QScrollArea):

    card_removed = Signal(Card)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.vly_m = QVBoxLayout()
        self.setLayout(self.vly_m)

        self.cw = QWidget(self)
        self.setWidget(self.cw)

        self.vly_cw = QVBoxLayout(self.cw)
        self.cw.setLayout(self.vly_cw)
        self.vly_cw.addStretch(1)

        self.cards: list[Card] = []

    def add_card(self, widget: QWidget = None, title: str = "", icon: QIcon = None) -> Card:
        card = Card(title, icon, parent=self)
        if widget is not None:
            card.set_central_widget(widget)
        card.pbn_close.clicked_with_item.connect(self.remove_card)
        self.vly_cw.insertWidget(self.vly_cw.count() - 1, card)
        self.cards.append(card)
        return card

    def remove_card(self, card: Card):
        self.vly_cw.removeWidget(card)
        self.cards.remove(card)
        card.deleteLater()

        self.card_removed.emit(card)
