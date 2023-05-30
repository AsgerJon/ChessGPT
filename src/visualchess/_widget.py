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


@PaintBoard()
class TestWidget(WhereMouse):
  """Widget test
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)
    self.setFixedSize(QSize(400, 400))
    """Decorated paint event"""
    ic(getattr(getattr(self, '__class__'), 'paintBoard'))

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Decorated paint event"""
    ic()
    painter = QPainter()
    painter.begin(self, )
    rect = painter.viewport()
    fitBoard = getattr(self, 'fitBoard')
    fitBoard(self.paintBoard, rect)
    paintStyles = getattr(self, 'paintStyles')
    painter.end()
