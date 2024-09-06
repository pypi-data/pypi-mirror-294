# coding: utf8
import sys
import time
import logging

try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError:
    try:
        from PySide2 import QtWidgets, QtCore, QtGui
    except ImportError:
        pass

from jnp3.gui import (
    CardsArea, Card, IconPushButton, StyleComboBox,
    DebugOutputButton, run_some_task, CheckUpdateButton,
    create_mono_icon, create_round_icon_from_pixmap,
    argb32_to_rgb,
)
from jnp3.misc import get_excepthook_for


class UiWg(object):

    def __init__(self, logger: logging.Logger, window: QtWidgets.QWidget):
        window.resize(540, 360)
        window.setWindowTitle("Style")

        self.lb_style = QtWidgets.QLabel("Style: ", window)
        self.cmbx_style = QtWidgets.QComboBox(window)
        self.cmbx_style.addItem("Default")
        self.cbx_use_std = QtWidgets.QCheckBox("Use style's standard palette", window)
        self.cbx_disable_wg = QtWidgets.QCheckBox("Disable widgets", window)

        self.pbn_svg = IconPushButton(watermelon_svg, parent=window)
        self.pbn_update = CheckUpdateButton(
            app_name="ChromHelper3",
            current_version="1.0.0",
            logger=logger,
            parent=window
        )

        icon1 = create_mono_icon(argb32_to_rgb(2 ** 32 + -13625057), "rect", 96)
        icon2 = create_mono_icon(argb32_to_rgb(2 ** 32 + -3413569), "round", 96)
        self.pbn_color1 = IconPushButton(icon1, parent=window)
        self.pbn_color2 = IconPushButton(icon2, parent=window)
        self.pbn_color3 = IconPushButton(create_round_icon_from_pixmap(icon1.pixmap(96, 96)), parent=window)

        self.hly_top = QtWidgets.QHBoxLayout()
        self.hly_top.addWidget(self.lb_style)
        self.hly_top.addWidget(self.cmbx_style)
        self.hly_top.addStretch(1)
        self.hly_top.addWidget(self.cbx_use_std)
        self.hly_top.addWidget(self.cbx_disable_wg)
        self.hly_top.addWidget(self.pbn_svg)
        self.hly_top.addWidget(self.pbn_update)
        self.hly_top.addWidget(self.pbn_color1)
        self.hly_top.addWidget(self.pbn_color2)
        self.hly_top.addWidget(self.pbn_color3)

        self.gbx_left = QtWidgets.QGroupBox("Group 1", window)
        self.rbn_1 = QtWidgets.QRadioButton("Radio button 1", self.gbx_left)
        self.rbn_2 = QtWidgets.QRadioButton("Radio button 2", self.gbx_left)
        self.rbn_3 = QtWidgets.QRadioButton("Radio button 3", self.gbx_left)
        self.cbx_tri = QtWidgets.QCheckBox("Tri-state check box", window)
        self.cbx_tri.setTristate(True)
        self.vly_gbx_left = QtWidgets.QVBoxLayout()
        self.vly_gbx_left.addWidget(self.rbn_1)
        self.vly_gbx_left.addWidget(self.rbn_2)
        self.vly_gbx_left.addWidget(self.rbn_3)
        self.vly_gbx_left.addWidget(self.cbx_tri)
        self.gbx_left.setLayout(self.vly_gbx_left)

        self.gbx_right = QtWidgets.QGroupBox("Group 2", window)
        self.pbn_1 = QtWidgets.QPushButton("Default push button", self.gbx_right)
        self.pbn_2 = QtWidgets.QPushButton("Toggle push button", self.gbx_right)
        self.pbn_3 = QtWidgets.QPushButton("Flat push button", self.gbx_right)
        self.pbn_2.setCheckable(True)
        self.pbn_2.setChecked(True)
        self.pbn_3.setFlat(True)
        self.vly_gbx_right = QtWidgets.QVBoxLayout()
        self.vly_gbx_right.addWidget(self.pbn_1)
        self.vly_gbx_right.addWidget(self.pbn_2)
        self.vly_gbx_right.addWidget(self.pbn_3)
        self.gbx_right.setLayout(self.vly_gbx_right)

        self.gbx_bot = QtWidgets.QGroupBox("Group 3", window)
        self.gbx_bot.setCheckable(True)
        self.gbx_bot.setChecked(False)
        self.lne_pswd = QtWidgets.QLineEdit("pass", self.gbx_bot)
        self.lne_pswd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.sbx_1 = QtWidgets.QSpinBox(self.gbx_bot)
        self.sbx_1.setValue(50)
        self.dte_1 = QtWidgets.QDateTimeEdit(self.gbx_bot)
        self.dte_1.setDateTime(QtCore.QDateTime.currentDateTime())

        self.hsd_1 = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.gbx_bot)
        self.hsb_1 = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Horizontal, self.gbx_bot)
        self.dia_1 = QtWidgets.QDial(self.gbx_bot)
        self.gly_gbx_bot = QtWidgets.QGridLayout()
        self.gly_gbx_bot.addWidget(self.hsd_1, 0, 0)
        self.gly_gbx_bot.addWidget(self.hsb_1, 1, 0)
        self.gly_gbx_bot.addWidget(self.dia_1, 0, 1, 0, 1)
        self.vly_gbx_bot = QtWidgets.QVBoxLayout()
        self.vly_gbx_bot.addWidget(self.lne_pswd)
        self.vly_gbx_bot.addWidget(self.sbx_1)
        self.vly_gbx_bot.addWidget(self.dte_1)
        self.vly_gbx_bot.addLayout(self.gly_gbx_bot)
        self.gbx_bot.setLayout(self.vly_gbx_bot)

        self.tabw_1 = QtWidgets.QTabWidget(window)
        self.tbw_1 = QtWidgets.QTableWidget(5, 5, window)
        self.txe_1 = QtWidgets.QTextEdit(window)
        self.tabw_1.addTab(self.tbw_1, "Table")
        self.tabw_1.addTab(self.txe_1, "Text Edit")

        self.gly_mid = QtWidgets.QGridLayout()
        self.gly_mid.addWidget(self.gbx_left, 0, 0)
        self.gly_mid.addWidget(self.gbx_right, 0, 1)
        self.gly_mid.addWidget(self.tabw_1, 1, 0)
        self.gly_mid.addWidget(self.gbx_bot, 1, 1)
        self.gly_mid.setRowStretch(0, 1)
        self.gly_mid.setRowStretch(1, 1)
        self.gly_mid.setColumnStretch(0, 1)
        self.gly_mid.setColumnStretch(1, 1)

        self.pgb_1 = QtWidgets.QProgressBar(window)
        self.pgb_1.setValue(15)
        self.pgb_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.vly_m = QtWidgets.QVBoxLayout()
        self.vly_m.addLayout(self.hly_top)
        self.vly_m.addLayout(self.gly_mid)
        self.vly_m.addWidget(self.pgb_1)

        window.setLayout(self.vly_m)


def some_func(logger: logging.Logger):
    for i in range(10):  # 假设要处理 10 个文件
        time.sleep(1)  # 模拟文件修改耗时
        message = f"文件 {i + 1}/10 已修改完成"
        logger.info(message)  # 记录日志


class Wg(QtWidgets.QWidget):

    def __init__(self, logger: logging.Logger, parent=None):
        super().__init__(parent)
        self.ui = UiWg(logger, self)
        self.logger = logger
        # self.vly_m = QtWidgets.QVBoxLayout()
        # self.setLayout(self.vly_m)
        #
        # self.pbn_1 = QtWidgets.QPushButton("hello", self)
        # self.vly_m.addWidget(self.pbn_1)
        # self.lne_1 = QtWidgets.QLineEdit("world", self)
        # self.vly_m.addWidget(self.lne_1)
        self.ui.pbn_svg.clicked.connect(self.on_pbn_svg_clicked)

    def on_pbn_svg_clicked(self):
        run_some_task("提示", "正在修改……", self, some_func, logger=self.logger)


# 图标来自 https://freeicons.io/profile/75801
watermelon_svg = """
<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <defs>
    <style>
      .cls-1 {
        fill: #00b277;
      }

      .cls-1, .cls-2, .cls-3, .cls-4, .cls-5, .cls-6, .cls-7 {
        stroke-width: 0px;
      }

      .cls-2 {
        fill: #424c63;
      }

      .cls-3 {
        fill: #a4ed70;
      }

      .cls-4 {
        fill: #d82b50;
      }

      .cls-5 {
        fill: #83d661;
      }

      .cls-6 {
        fill: #00d18d;
      }

      .cls-7 {
        fill: #ff3b65;
      }
    </style>
  </defs>
  <path class="cls-6" d="M37.001,3.295c.399-.399,1.049-.394,1.431.021,8.988,9.749,8.751,24.943-.711,34.406-9.462,9.462-24.656,9.699-34.406.711-.415-.382-.42-1.032-.021-1.431C7.835,32.46,32.46,7.836,37.001,3.295Z"></path>
  <path class="cls-1" d="M37.721,37.721c3.455-3.455,5.674-7.675,6.669-12.114-1.062,1.976-2.422,3.833-4.09,5.501-8.821,8.821-22.906,9.159-32.136,1.023l-4.87,4.87c-.399.399-.394,1.049.021,1.431,9.749,8.988,24.943,8.751,34.406-.711Z"></path>
  <path class="cls-3" d="M3.989,36.307c8.924,8.924,23.393,8.924,32.318,0s8.924-23.393,0-32.318L3.989,36.307Z"></path>
  <path class="cls-5" d="M8.164,32.131l-4.175,4.175c8.924,8.924,23.393,8.924,32.318,0,1.521-1.521,2.777-3.206,3.78-4.995-8.833,8.617-22.765,8.89-31.922.82Z"></path>
  <path class="cls-7" d="M6.11,34.185c7.753,7.753,20.322,7.753,28.075,0s7.753-20.322,0-28.075L6.11,34.185Z"></path>
  <path class="cls-4" d="M8.164,32.131l-2.054,2.054c6.71,6.71,17.023,7.601,24.704,2.696-7.652,2.43-16.299.848-22.65-4.75Z"></path>
  <path class="cls-2" d="M27.926,27.926c.391-.391,1.024-.39,1.414,0l.707.707c.39.39.391,1.023,0,1.414s-1.024.39-1.414,0l-.707-.707c-.39-.39-.391-1.023,0-1.414Z"></path>
  <path class="cls-2" d="M21.525,31.258c.14-.14.322-.24.532-.277.543-.096,1.062.267,1.159.811l.174.985c.097.543-.266,1.062-.811,1.159-.543.096-1.062-.267-1.159-.811l-.174-.985c-.059-.334.055-.659.278-.882Z"></path>
  <path class="cls-2" d="M14.369,30.316c.289-.289.739-.382,1.13-.199.501.233.717.828.484,1.328l-.422.906c-.232.504-.829.717-1.329.484-.501-.233-.717-.828-.484-1.328l.422-.906c.051-.109.119-.205.199-.286Z"></path>
  <path class="cls-2" d="M31.258,21.525c.223-.223.548-.337.882-.278l.985.174c.544.096.907.615.811,1.159-.096.544-.615.907-1.159.811l-.985-.174c-.544-.096-.907-.615-.811-1.159.037-.21.137-.392.277-.532Z"></path>
  <path class="cls-2" d="M30.316,14.369c.08-.08.176-.148.286-.199l.906-.422c.5-.233,1.095-.017,1.328.484.233.5.02,1.096-.484,1.329l-.906.422c-.5.233-1.095.017-1.328-.484-.183-.391-.09-.841.199-1.13Z"></path>
</svg>
"""


class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        sys.excepthook = get_excepthook_for(self.logger)

        self.vly_m = QtWidgets.QVBoxLayout()
        self.setLayout(self.vly_m)

        self.ca = CardsArea(self)
        self.ca.card_removed.connect(self.on_card_removed)
        self.vly_m.addWidget(self.ca)

        self.c1 = self.ca.add_card(Wg(self.logger, self), "示例1", QtGui.QIcon("chrome_32.png"))
        self.c2 = self.ca.add_card(StyleComboBox(0, parent=self), "示例2")
        self.c3 = self.ca.add_card(title="示例3", icon=QtGui.QIcon("chrome_32.png"))
        self.ca.add_card(DebugOutputButton(self.logger, text="打开调试窗口", parent=self), "调试窗口")

        self.logger.warning("hahahah")
        self.logger.error("hehehe")

    def sizeHint(self):
        return QtCore.QSize(860, 640)

    def on_card_removed(self, card: Card):
        self.logger.info(card.title)
        print(1 / 0)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    win = MainWindow()
    win.show()
    if hasattr(app, "exec"):
        app.exec()
    else:
        app.exec_()
