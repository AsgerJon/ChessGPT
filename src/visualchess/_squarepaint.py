"""SquarePaint is responsible for applying painting operations on the
StaticBoard on a square by square basis"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize, QRect, QPoint
from PySide6.QtGui import QPaintEvent, QPainter, QPixmap
from icecream import ic
from worktoy.core import maybe

from visualchess import Square
from workstyle import WhereMouse
from workstyle.styles import BezelStyle, GridStyle, FileData, BoardDims

ic.configureOutput(includeContext=True)


class SquarePaint(WhereMouse):
  """SquarePaint is responsible for applying painting operations on the
  StaticBoard on a square by square basis.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)
    self._pixMaps = None
    self.setMinimumSize(QSize(400, 400))
    self.click.connect(self.debug)
    self.doubleClick.connect(self.debug2)
    self._boardPix = None

  def debug(self, *_) -> NoReturn:
    """Debug"""

  def debug2(self, *_) -> NoReturn:
    """Debug"""

  def lockSize(self) -> NoReturn:
    """Locks the resize flag"""

  def unlockSize(self) -> NoReturn:
    """Unlocks the resize flag"""

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """First calls the parent paintEvent before applying the context
    specific operation"""
    painter = QPainter()
    painter.begin(self)
    view = painter.viewport()
    BezelStyle @ painter
    rX, rY = BoardDims.cornerRadiusX, BoardDims.cornerRadiusY
    painter.drawRoundedRect(Square.fitSquareRect(view), rX, rY, )
    GridStyle @ painter
    boardRect = Square.fitSquareMarginsRect(view)
    painter.drawRect(boardRect)
    for square in Square:
      square.applyPaint(painter)
    painter.end()
