# coding: utf8
import sys
import json
import requests
from logging import Logger

from .._compat import (
    Qt,
    QIcon, QPixmap,
    QMessageBox, QPushButton, QWidget,
)
from ..thread import run_some_task
from jnp3.misc import FakeLogger


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

        msg_box = QMessageBox(self.wg_parent)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("提示")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(f"发现新版本：v{self.latest_version}。"
                        f"点击 <a href='{self.download_url}' style='text-decoration: none; color: red'>下载</a>。")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        if hasattr(msg_box, "exec"):
            msg_box.exec()
        else:
            msg_box.exec_()

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

            download_url = update_info[latest_version][sys.platform]
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
