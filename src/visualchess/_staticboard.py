"""StaticBoard draws a chess board."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QMarginsF, QRect, QPoint, QSize
from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtWidgets import QWidget
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from visualchess.styles import BackgroundStyle, BezelStyle, \
  LightSquareStyle, \
  DarkSquareStyle

origin = QPoint(0, 0)
gridWidth = 3


class StaticBoard(QWidget):
  """StaticBoard draws a chess board.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QWidget.__init__(self, parent)
    self._bezelMargins = QMarginsF(16, 16, 16, 16, )
    self._recursionPaintFlag = False

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation of paint event"""
    size = event.rect().size()
    if (size.width() - size.height()) ** 2 > 4:
      if self._recursionPaintFlag:
        raise RecursionError('Recursion in resizing of paint view port')
      size = QSize(size.width(), size.height())
      newRect = QRect(origin, size)
      newRect.moveCenter(event.rect().center())
      self._recursionPaintFlag = True
      return self.paintEvent(QPaintEvent(QRect))
    self._recursionPaintFlag = True
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    boardRect = viewRect - self._bezelMargins
    boardSide = min(boardRect.width(), boardRect.height()) - gridWidth * 7
    squareSide = boardSide // 8
    boardSide = 8 * squareSide
    boardRect = QRect(origin, QSize(boardSide, boardSide))
    boardRect.moveCenter(viewRect.center())
    boardTopLeft = boardRect.topLeft()
    #  Paint the bezels
    painter = BezelStyle @ painter
    painter.drawRoundedRect(viewRect, gridWidth, gridWidth)
    #  Collect light and dark squares
    darkSquares, lightSquares = [], []
    left, top = boardTopLeft.left(), boardTopLeft.top()
    side = squareSide
    size = QSize(side, side)
    for i in range(8 * 8):
      leftTop = QPoint((i % 8) * side + left, (i // 8) * side + top)
      if (i * (i // 8)) % 4 and (i * (i // 8) + i + (i // 8) + 1) % 4:
        lightSquares.append(QRect(leftTop, size))
      else:
        darkSquares.append(QRect(leftTop, size))
    LightSquareStyle @ painter
    painter.drawRects(lightSquares)
    DarkSquareStyle @ painter
    painter.drawRects(lightSquares)
    painter.end()
