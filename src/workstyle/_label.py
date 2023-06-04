"""Label tests mixins"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic

from workstyle import WhereMouse
from workstyle.stylesettings import lightSquareStyle

ic.configureOutput(includeContext=True)


class Label(WhereMouse):
  """LOL"""

  def __init__(self, *args, **kwargs) -> None:
    self._number = 0
    self._label = None
    self._layout = None
    WhereMouse.__init__(self, *args, **kwargs)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation"""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    lightSquareStyle @ painter
    painter.drawRoundedRect(viewRect, 0, 0)
    painter.end()
