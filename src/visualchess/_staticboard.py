"""StaticBoard draws a chess board."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QMarginsF, QRect, QPoint, QSize, QMargins, \
  QPointF, QRectF, QSizeF, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QResizeEvent
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from workstyle import WhereMouse
from workstyle.styles import BezelStyle, LightSquareStyle, DarkSquareStyle, \
  GridStyle

ic.configureOutput(includeContext=True)

origin = QPointF(0, 0)
gridWidth = 3
leftMargin, topMargin, rightMargin, bottomMargin = 16, 16, 16, 16
Squares = tuple[list[QRectF], list[QRectF]]


class StaticBoard(WhereMouse):
  """StaticBoard draws a chess board.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  boardSize = Signal(QSizeF)

  @staticmethod
  def squareCenter(viewPort: QRectF) -> QRect:
    """Returns a square QRect fitted centrally in the viewPort."""
    side = min(viewPort.height(), viewPort.width(), )
    rect = QRectF(origin, QSizeF(side, side))
    rect.moveCenter(viewPort.center())
    ic(rect)
    return rect

  @staticmethod
  def removeBezels(source: QRectF, ) -> QRect:
    """Returns a new QRect with the bezels removed. Please note that the
    rect will be moved back to the center of the source."""
    height = source.height() - topMargin - bottomMargin
    width = source.width() - leftMargin - rightMargin
    rect = QRectF(origin, QSizeF(width, height))
    rect.moveCenter(source.center())
    ic(rect)
    return rect

  @staticmethod
  def collectSquares(boardRect: QRectF, ) -> Squares:
    """Distributes squares across the board"""
    center = boardRect.center()
    boardHeight = boardRect.height() - (boardRect.height() % 8)
    boardSize = QSizeF(boardHeight, boardHeight)
    boardRect = QRectF(origin, boardSize)
    boardRect.moveCenter(center)
    ic(boardRect)
    left, top = boardRect.left(), boardRect.top(),
    left = left + 1
    top = top + 1
    squareSize = QSizeF(1, 1) * int(boardRect.height() // 8 - gridWidth)
    darkSquares, lightSquares = [], []
    step = squareSize.height() + gridWidth
    for i in range(8):
      for j in range(8):
        leftTop = QPointF(left + step * i, top + step * j)
        if i % 2 == j % 2:
          lightSquares.append(QRectF(leftTop, squareSize))
        else:
          darkSquares.append(QRectF(leftTop, squareSize))
    return (lightSquares, darkSquares)

  def __init__(self, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QWidget.__init__(self, )
    self.setMouseTracking(True)
    self._bezelMargins = QMarginsF(16, 16, 16, 16, )
    self._radius = 8
    self._recursionPaintFlag = False
    self.setMinimumSize(QSize(400, 400))

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation of painting"""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.Antialiasing)
    viewSquare = QRectF(self.squareCenter(painter.viewport()))
    self.boardSize.emit(viewSquare.size())
    boardRect = QRectF(self.removeBezels(viewSquare, ))
    boardHeight = boardRect.height()
    boardRect = QRectF(origin, QSizeF(boardHeight, boardHeight))
    boardRect.moveCenter(viewSquare.center())
    lightSquares, darkSquares = self.collectSquares(boardRect, )
    boardHeight = lightSquares[0].height() * 8 + 7 * gridWidth
    left = max(lightSquares[0].left(), darkSquares[0].left())
    top = max(lightSquares[0].top(), darkSquares[0].top())
    right = max(lightSquares[-1].right(), darkSquares[-1].right())
    bottom = max(lightSquares[-1].bottom(), darkSquares[-1].bottom())
    width = right - left
    height = bottom - top
    boardSize = QSizeF(width, height)
    boardTopLeft = QPointF(left, top)
    boardRect = QRectF(boardTopLeft, boardSize)
    boardRect = lightSquares[0].united(lightSquares[-1])

    #  Paint the bezels
    BezelStyle @ painter
    painter.drawRoundedRect(viewSquare, self._radius, self._radius)
    #  Paints gridlines
    GridStyle @ painter
    painter.drawRect(boardRect)
    #  Paints light and dark squares
    LightSquareStyle @ painter
    painter.drawRects(lightSquares)
    DarkSquareStyle @ painter
    painter.drawRects(darkSquares)

    painter.end()

  def resizeEvent(self, event: QResizeEvent) -> NoReturn:
    """Triggers update of statusBar"""
    # self.boardSize.emit(viewSquare.size().toSizeF())
