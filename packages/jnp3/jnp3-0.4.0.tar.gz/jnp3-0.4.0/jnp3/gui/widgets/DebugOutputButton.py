# coding: utf8
from logging import (
    Logger, Handler, LogRecord,
    Formatter,
)
from .._compat import (
    Qt, QSize,
    QCloseEvent, QIcon, QPixmap,
    QDialog, QPushButton, QTextEdit, QVBoxLayout, QWidget,
)


DEBUG_OUTPUT_CACHE = []


class GlobalOutputHandler(Handler):

    def __init__(self, level: int | str = 0):
        super().__init__(level)

    def emit(self, record: LogRecord):
        msg = self.format(record)
        DEBUG_OUTPUT_CACHE.append(msg)


class TextEditHandler(Handler):

    def __init__(self, txe_wg: QTextEdit, level: int | str = 0):
        super().__init__(level=level)
        self.txe_wg = txe_wg

    def emit(self, record: LogRecord):
        msg = self.format(record)
        self.txe_wg.append(msg)
        self.txe_wg.moveCursor(self.txe_wg.textCursor().MoveOperation.End)


class DaDebugOutput(QDialog):

    def __init__(
            self,
            logger: Logger,
            formatter: Formatter,
            level: int | str = 0,
            parent: QWidget = None
    ):
        super().__init__(parent)
        self.logger = logger

        # ============== UI =================
        self.vly_m = QVBoxLayout()
        self.setLayout(self.vly_m)

        self.txe_m = QTextEdit(self)
        self.txe_m.setReadOnly(True)

        self.vly_m.addWidget(self.txe_m)

        # ============ END UI ===============

        self.load_previous_output()

        self.handler_txe = TextEditHandler(self.txe_m, level)
        self.handler_txe.setFormatter(formatter)
        self.logger.addHandler(self.handler_txe)

    def sizeHint(self):
        return QSize(600, 300)

    def closeEvent(self, event: QCloseEvent):
        self.logger.removeHandler(self.handler_txe)
        event.accept()

    def load_previous_output(self):
        """将之前缓存的输出加载到 QTextEdit 中"""
        for text in DEBUG_OUTPUT_CACHE:
            self.txe_m.append(text)
        self.txe_m.moveCursor(self.txe_m.textCursor().MoveOperation.End)


class DebugOutputButton(QPushButton):

    def __init__(
            self,
            logger: Logger,
            formatter: str | Formatter = None,
            text: str = "打开输出窗口",
            icon: QIcon | QPixmap = None,
            parent: QWidget = None,
    ):
        if icon is None:
            super().__init__(text=text, parent=parent)
        else:
            super().__init__(icon=icon, text=text, parent=parent)

        self.logger = logger
        if formatter is None:
            self.formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
        elif isinstance(formatter, Formatter):
            self.formatter = formatter
        elif isinstance(formatter, str):
            self.formatter = Formatter(formatter)
        else:
            raise ValueError("Unsupported formatter type")

        self.gbo_handler = GlobalOutputHandler(level=self.logger.level)
        self.gbo_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.gbo_handler)

        self.clicked.connect(self.on_self_clicked)

    def on_self_clicked(self):
        dd = DaDebugOutput(
            self.logger,
            self.formatter,
            self.logger.level,
            parent=self
        )
        dd.setWindowTitle("输出窗口")
        dd.setWindowModality(Qt.WindowModality.NonModal)
        dd.show()
