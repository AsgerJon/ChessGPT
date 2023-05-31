"""Widget test"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize
from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic

from visualchess import PaintBoard
from workstyle import WhereMouse
from workstyle.styles import BezelStyle

ic.configureOutput(includeContext=True)


class TestWidget(WhereMouse):
  """Widget test
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Decorated paint event"""
