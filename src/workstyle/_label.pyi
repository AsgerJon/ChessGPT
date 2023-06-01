from PySide6.QtGui import QPaintEvent
from typing import NoReturn
from workstyle import WhereMouse as WhereMouse
from workstyle.styles import LightSquareStyle as LightSquareStyle

class Label(WhereMouse):
    def __init__(self, *args, **kwargs) -> None: ...
    def paintEvent(self, event: QPaintEvent) -> NoReturn: ...
