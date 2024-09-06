# coding: utf8
import sys
import json
import requests
import subprocess
from logging import Logger

from .._compat import (
    Qt, QSize,
    QIcon, QPixmap,
    QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)
from ..misc import get_exec
from ..thread import run_some_task
from ..icon import get_icon_from_svg
from jnp3.misc import FakeLogger


# 来自 https://freeicons.io/profile/726
info_svg = """
<svg version="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" enable-background="new 0 0 48 48">
    <circle fill="#2196F3" cx="24" cy="24" r="21"></circle>
    <rect x="22" y="22" fill="#fff" width="4" height="11"></rect>
    <circle fill="#fff" cx="24" cy="16.5" r="2.5"></circle>
</svg>
"""


class LinkDialog(QDialog):

    def __init__(
            self,
            latest_version: str,
            download_url: str,
            parent: QWidget = None
    ):
        super().__init__(parent)

        self.setWindowTitle("提示")
        self.vly_m = QVBoxLayout(self)
        self.setLayout(self.vly_m)

        self.hly_top = QHBoxLayout()
        self.vly_m.addLayout(self.hly_top)

        self.lb_icon = QLabel(self)
        self.lb_icon.setPixmap(get_icon_from_svg(info_svg, 40, 40).pixmap(40, 40))
        self.hly_top.addWidget(self.lb_icon)

        self.lb_text = QLabel(self)
        self.lb_text.setTextFormat(Qt.TextFormat.RichText)
        self.lb_text.setText(
            f"发现新版本：v{latest_version}。"
            f"点击 <a href='{download_url}' style='text-decoration: none; color: red'>下载</a>。"
        )
        self.lb_text.setOpenExternalLinks(True)  # 允许打开外部链接
        self.hly_top.addWidget(self.lb_text)

        self.hly_bot = QHBoxLayout()
        self.vly_m.addLayout(self.hly_bot)
        self.hly_bot.addStretch(1)

        self.pbn_ok = QPushButton("Ok", self)
        self.pbn_ok.clicked.connect(self.accept)
        self.hly_bot.addWidget(self.pbn_ok)

    def sizeHint(self):
        return QSize(100, 10)


class CheckUpdateButton(QPushButton):

    def __init__(
            self,
            app_name: str,
            current_version: str,
            update_url: str = None,
            logger: Logger | FakeLogger = None,
            text: str = "检查更新",
            icon: QIcon | QPixmap = None,
            parent: QWidget = None,
    ):
        if icon is None:
            super().__init__(text=text, parent=parent)
        else:
            super().__init__(icon=icon, text=text, parent=parent)

        self.wg_parent = parent
        if update_url is None:
            update_url = f"https://karlblue.github.io/update_repo/{app_name}.json"
        self.update_url = update_url
        self.app_name = app_name
        self.current_version = current_version
        self.logger = logger or FakeLogger()

        # ========= 检查更新时用到 =============
        self.has_update = False
        self.msg_when_no_update = ""  # 当无需更新或者检车更新失败时的提示信息
        self.download_url = ""        # 当需要更新时的下载链接
        self.latest_version = ""      # 当需要更新时的新版本号
        # =====================================

        self.clicked.connect(self.on_self_clicked)

    def on_self_clicked(self):
        run_some_task("更新", "正在检查更新……", self, self.check_update)

        if self.has_update is False:
            QMessageBox.information(self, "提示", self.msg_when_no_update)
            return

        msg_box = LinkDialog(self.latest_version, self.download_url, self.wg_parent)
        get_exec(msg_box)()

    def check_update(self):
        try:
            response = requests.get(self.update_url, timeout=10)
            response.raise_for_status()

            update_info = json.loads(response.text)

            latest_version = update_info["latest"]
            if self.compare_versions(latest_version, self.current_version) != 1:
                # 最新的版本不比当前版本大
                self.has_update = False
                self.msg_when_no_update = "当前已是最新版本。"
                return

            if sys.platform != "darwin":
                download_url = update_info[latest_version][sys.platform]
            else:
                inner = update_info[latest_version][sys.platform]
                if isinstance(inner, dict):
                    mac_ver = subprocess.check_output(["sw_vers", "-productVersion"]).decode("utf8").strip()
                    if mac_ver.startswith("10."):
                        download_url = inner["10"]
                    else:
                        download_url = inner["11"]
                else:
                    download_url = inner
            self.has_update = True
            self.download_url = download_url
            self.latest_version = latest_version

        except requests.exceptions.RequestException as e:
            self.has_update = False
            self.msg_when_no_update = f"网络请求出错。"
            self.logger.error(e)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.has_update = False
            self.msg_when_no_update = f"更新文件格式有误或不支持当前系统。"
            self.logger.error(e)
        except Exception as e:
            self.has_update = False
            self.msg_when_no_update = f"出现未知错误。"
            self.logger.error(e)

    @staticmethod
    def compare_versions(v1: str, v2: str) -> int:
        v1_t = tuple(map(int, v1.split(".")))
        v2_t = tuple(map(int, v2.split(".")))
        if v1_t < v2_t:
            return -1
        elif v1_t > v2_t:
            return 1
        else:
            return 0
