# coding: utf8
import sys
import json
import tempfile
import requests
import py7zr
import subprocess
from logging import Logger
from pathlib import Path

from .._compat import (
    QIcon, QPixmap,
    QApplication, QMessageBox, QPushButton, QWidget,
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

        # ========= 下载更新时用到 =============
        self.download_success = False
        self.msg_after_download = ""  # 运行 download_update 后的信息
        self.update_exe_file = ""     # 用于更新的脚本
        # =====================================

        self.clicked.connect(self.on_self_clicked)

    def on_self_clicked(self):
        run_some_task("更新", "正在检查更新……", self, self.check_update)

        if self.has_update is False:
            QMessageBox.information(self, "提示", self.msg_when_no_update)
            return

        r = QMessageBox.question(self, "提示", f"发现新版本：v{self.latest_version}，是否更新？")
        if r == QMessageBox.StandardButton.No:
            return

        run_some_task("更新", "正在下载更新……", self, self.download_update)

        if self.download_success is False:
            QMessageBox.information(self, "提示", self.msg_after_download)
            return

        r = QMessageBox.question(self, "提示", "已下载更新，点击 Yes 将关闭软件执行更新。")
        if r == QMessageBox.StandardButton.No:
            return

        self.install_update()

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

    def download_update(self):
        if len(self.download_url) == 0:
            self.download_success = False
            self.msg_after_download = "没有下载链接。"
            return

        temp_dir = tempfile.gettempdir()
        outer_dir = Path(temp_dir, f"{self.app_name}.info")
        outer_dir.mkdir(parents=True, exist_ok=True)

        save_path = outer_dir / f"{self.app_name}.data"

        try:
            response = requests.get(self.download_url, stream=True)

            # 下载
            with open(save_path, "wb") as f:
                for data in response.iter_content(1024):
                    f.write(data)
            # 解压
            with py7zr.SevenZipFile(save_path, mode="r") as a:
                a.extractall(path=outer_dir)
            # 创建复制脚本
            if sys.platform == "win32":
                lines = [
                    "@echo off",
                    "timeout /t 1 /nobreak",
                    # 这里就要求解压出来单个目录，且于应用名称相同
                    f'xcopy /E /Y "{outer_dir / self.app_name}" "{Path(sys.executable).parent}"',
                ]
                self.update_exe_file = str(outer_dir / "update.bat")
            elif sys.platform == "darwin":
                src_file = outer_dir / f"{self.app_name}.app"
                lines = [
                    "#!/bin/zsh",
                    "sleep 1",
                    # parent-dir/xx.app/Contents/MacOS/xxx
                    f'cp -R "{src_file}" "{Path(sys.executable).parent.parent.parent.parent}"',
                ]
                self.update_exe_file = str(outer_dir / "update.sh")
            else:
                self.download_success = False
                self.msg_after_download = "不支持的系统。"
                return

            with open(self.update_exe_file, "w") as s:
                s.write("\n".join(lines))

            self.download_success = True

        except requests.exceptions.RequestException as e:
            self.download_success = False
            self.msg_after_download = "网络请求出错。"
            self.logger.error(e)
        except py7zr.Bad7zFile as e:
            self.download_success = False
            self.msg_after_download = "不是有效的 .7z 文件，或文件已损坏。"
            self.logger.error(e)
        except OSError as e:
            self.download_success = False
            self.msg_after_download = "文件操作时出错。"
            self.logger.error(e)
        except MemoryError as e:
            self.download_success = False
            self.msg_after_download = "解压过程中内存不足。"
            self.logger.error(e)
        except Exception as e:
            self.download_success = False
            self.msg_after_download = "出现未知错误。"
            self.logger.error(e)

    def install_update(self):
        if sys.platform == "win32":
            subprocess.Popen(
                [self.update_exe_file],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            QApplication.quit()
        elif sys.platform == "darwin":
            subprocess.Popen(
                ["zsh", self.update_exe_file],
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            QApplication.quit()
