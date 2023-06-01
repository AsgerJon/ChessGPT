from PySide6.QtGui import QPaintEvent
from typing import NoReturn
from workstyle import WhereMouse

class TestWidget(WhereMouse):
    def __init__(self, *args, **kwargs) -> None: ...
    def paintEvent(self, event: QPaintEvent) -> NoReturn: ...
