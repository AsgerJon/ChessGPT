"""StaticBoard draws a chess board."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QMarginsF, QRect, QPoint, QSize
from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from visualchess import MouseTrackerMixin
from workstyle.styles import BezelStyle, LightSquareStyle, DarkSquareStyle

origin = QPoint(0, 0)
gridWidth = 3

ic.configureOutput(includeContext=True)


class StaticBoard(QWidget, MouseTrackerMixin):
  """StaticBoard draws a chess board.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QWidget.__init__(self, )
    self.setMouseTracking(True)
    self._bezelMargins = QMarginsF(16, 16, 16, 16, )
    self._recursionPaintFlag = False
    self.setMinimumSize(QSize(256, 256))

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation of painting"""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    viewCenter = viewRect.center()
    s = min(viewRect.height(), viewRect.width(), )
    viewSize = QSize(s, s)
    viewRect = QRect(origin, viewSize)
    baseRect = QRect(origin, viewSize)
    viewRect.moveCenter(viewCenter)
    boardCenter = viewRect.center()
    boardRect = viewRect
    boardSize = boardRect.size() - QSize(32, 32)
    boardRect.setSize(boardSize)
    boardRect.moveCenter(boardCenter)
    boardSide = min(boardRect.width(), boardRect.height()) - gridWidth * 7
    squareSide = boardSide // 8
    boardSide = 8 * squareSide
    boardRect = QRect(origin, QSize(boardSide, boardSide))
    boardRect.moveCenter(viewRect.center())
    boardTopLeft = boardRect.topLeft()
    #  Paint the bezels
    painter = BezelStyle @ painter
    baseRect.moveCenter(boardRect.center())
    painter.drawRoundedRect(baseRect, gridWidth, gridWidth)
    #  Collect light and dark squares
    darkSquares, lightSquares = [], []
    left, top = boardTopLeft.x(), boardTopLeft.y()
    side = squareSide
    size = QSize(side, side)
    for i in range(8):
      for j in range(8):
        leftTop = QPoint(left + side * i, top + side * j)
        if i % 2 == j % 2:
          lightSquares.append(QRect(leftTop, size))
        else:
          darkSquares.append(QRect(leftTop, size))

    LightSquareStyle @ painter
    painter.drawRects(lightSquares)
    DarkSquareStyle @ painter
    painter.drawRects(darkSquares)
    painter.end()
