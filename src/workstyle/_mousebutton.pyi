from PySide6.QtCore import QObject
from PySide6.QtGui import QMouseEvent
from _typeshed import Incomplete
from typing import NoReturn
from worktoy.core import maybe as maybe

class MouseButton(QObject):
    click: Incomplete
    doubleClick: Incomplete
    pressHold: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, event: QMouseEvent) -> bool: ...
    def mousePressEvent(self, event: QMouseEvent) -> NoReturn: ...
    def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn: ...
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> NoReturn: ...
