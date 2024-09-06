# coding: utf8
has_pyside6 = False
has_pyside2 = False

try:
    import PySide6

    has_pyside6 = True

    from PySide6.QtCore import (
        Qt,
        QAbstractListModel,
        QByteArray,
        QModelIndex,
        QObject,
        QSize,
        QThread,
        Signal,
    )
    from PySide6.QtGui import (
        QBrush,
        QCloseEvent,
        QColor,
        QIcon,
        QKeyEvent,
        QPainter,
        QPixmap,
    )
    from PySide6.QtWidgets import (
        QApplication,
        QComboBox,
        QDialog,
        QFrame,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QMessageBox,
        QPushButton,
        QScrollArea,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
    from PySide6.QtSvg import (
        QSvgRenderer
    )
    from PySide6 import __version__ as pyside_version
except ImportError:
    try:
        import PySide2

        has_pyside2 = True

        from PySide2.QtCore import (
            Qt,
            QAbstractListModel,
            QByteArray,
            QModelIndex,
            QObject,
            QSize,
            QThread,
            Signal,
        )
        from PySide2.QtGui import (
            QBrush,
            QCloseEvent,
            QColor,
            QIcon,
            QKeyEvent,
            QPainter,
            QPixmap,
        )
        from PySide2.QtWidgets import (
            QApplication,
            QComboBox,
            QDialog,
            QFrame,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QMessageBox,
            QPushButton,
            QScrollArea,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )
        from PySide2.QtSvg import (
            QSvgRenderer
        )
        from PySide2 import __version__ as pyside_version

    except ImportError:
        pyside_version = "0.0.0"

__all__ = ["has_pyside6", "has_pyside2", "pyside_version"]

__all__ += [
    # QtCore
    "Qt",
    "QAbstractListModel",
    "QByteArray",
    "QModelIndex",
    "QObject",
    "QSize",
    "QThread",
    "Signal",
    # QtGui
    "QBrush",
    "QCloseEvent",
    "QColor",
    "QIcon",
    "QKeyEvent",
    "QPainter",
    "QPixmap",
    # QtWidgets
    "QApplication",
    "QComboBox",
    "QDialog",
    "QFrame",
    "QGroupBox",
    "QHBoxLayout",
    "QLabel",
    "QMessageBox",
    "QPushButton",
    "QScrollArea",
    "QTextEdit",
    "QVBoxLayout",
    "QWidget",
    # QtSvg
    "QSvgRenderer",
]
