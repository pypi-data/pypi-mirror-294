# coding: utf8
import sys
from .._compat import (
    Qt, QAbstractListModel, QModelIndex, QObject,
    QApplication, QComboBox, QWidget,
    pyside_version,
)


class _StyleListModel(QAbstractListModel):

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        if sys.platform == "win32":
            self.styles = ["windowsvista", "Fusion", "Windows"]
            ver = list(map(lambda s: int(s), pyside_version.split(".")))
            if ver >= [6, 7, 0]:
                self.styles.insert(0, "windows11")
        elif sys.platform == "darwin":
            self.styles = ["macOS", "Fusion", "Windows"]
        elif sys.platform == "linux":
            self.styles = ["Fusion", "Windows"]
        else:
            self.styles = []

    def rowCount(self, parent: QModelIndex = ...):
        return len(self.styles)

    def data(self, index: QModelIndex, role: int = ...):
        row = index.row()

        if role == Qt.ItemDataRole.DisplayRole:
            return self.styles[row]


class StyleComboBox(QComboBox):

    def __init__(self, default_style: int = 0, parent: QWidget = None):
        super().__init__(parent)
        self.setModel(_StyleListModel(self))
        self.currentIndexChanged.connect(self.on_self_current_index_changed)

        self.setCurrentIndex(default_style)

    def on_self_current_index_changed(self, index: int):
        model = self.model()
        idx = model.index(index, 0)
        if idx.isValid():
            style = model.data(idx, Qt.ItemDataRole.DisplayRole)
            QApplication.setStyle(style)
