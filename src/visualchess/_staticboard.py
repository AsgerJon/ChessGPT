"""StaticBoard draws the chessboard"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize
from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic

from visualchess import PaintBoard
from workstyle.styles import BezelStyle, GridStyle, LightSquareStyle, \
  DarkSquareStyle

ic.configureOutput(includeContext=True)


class StaticBoard(PaintBoard):
  """StaticBoard draws the chessboard
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    PaintBoard.__init__(self, *args, **kwargs)
    self.setMinimumSize(QSize(400, 400))

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementing the paint event"""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    self._outerRectangle = painter.viewport()
    bezel = self.getBaseRect()
    board = self.getBoardRect()
    light, dark = self.collectSquares()
    BezelStyle @ painter
    painter.drawRoundedRect(bezel, 16, 16, )
    GridStyle @ painter
    painter.drawRect(board)
    LightSquareStyle @ painter
    painter.drawRects(light)
    DarkSquareStyle @ painter
    painter.drawRects(dark)
    painter.end()
