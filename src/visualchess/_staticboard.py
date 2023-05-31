"""StaticBoard draws the chessboard"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize, QPointF, QRectF
from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic
from worktoy.core import plenty
from worktoy.stringtools import stringList

from visualchess import chessBoardFunc
from workstyle import WhereMouse
from workstyle.styles import BezelStyle, GridStyle, LightSquareStyle, \
  DarkSquareStyle

ic.configureOutput(includeContext=True)


class StaticBoard(WhereMouse):
  """StaticBoard draws the chessboard
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)
    self._baseSize = QSize(400, 400)
    self.setMinimumSize(self._baseSize)
    self._allowResize = True
    self._fixedSize = QSize(400, 400)

  def lockSize(self) -> NoReturn:
    """Method locking the widget at its present size"""
    self._fixedSize = self.geometry().size()
    self._allowResize = False

  def unlockSize(self) -> NoReturn:
    """Method unlocking the widget allowing resizing"""
    self.setMinimumSize(self._baseSize)
    self._allowResize = True

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementing the paint event"""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    fixedRect = QRectF(QPointF(0., 0.), self._fixedSize)
    rect = painter.viewport() if self._allowResize else fixedRect
    rects = chessBoardFunc(rect, gridRatio=16 / 400)
    styles = dict(
      light=LightSquareStyle, dark=DarkSquareStyle,
      bezel=BezelStyle, grid=GridStyle, )
    keys = stringList('bezel, grid, light, dark')
    for key in keys:
      style, rect = styles.get(key, None), rects.get(key, None)
      if not plenty(style, rect):
        raise ValueError()
      style @ painter
      painter.drawRects(rect)
    painter.end()
