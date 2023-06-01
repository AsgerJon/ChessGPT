from PySide6.QtCore import QObject, QPoint as QPoint, QPointF, Qt as Qt
from _typeshed import Incomplete
from typing import NoReturn

class MouseLocation(QObject):
    cursorMove: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def setPoint(self, point: QPointF) -> NoReturn: ...
