"""BoardMouse is a subclass of BoardWidget that provides the mouse related
logic."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string
from typing import NoReturn

from PySide6.QtCore import Qt, QPointF, QRectF, QSizeF
from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic

from workstyle import CoreWidget
from workstyle.stylesettings import backgroundStyle, bezelStyle, \
  labelStyle, \
  outlineStyle, gridStyle, darkSquareStyle, lightSquareStyle

ic.configureOutput(includeContext=True)


class BoardLayout(CoreWidget):
  """BoardMouse is a subclass of BoardWidget that provides the mouse related
  logic.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _bezelRatio = 0.08
  _squareGap = 2
  _boardOutline = 2
  _cornerRadius = 8
  _adjustFontSize = 1 / 600
  _origin = QPointF(0, 0)

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self._painterViewPort = []

  def getViewPort(self) -> QRectF:
    """This method predicts the viewport on the widget"""
    if self._painterViewPort:
      return self._painterViewPort.pop()
    return self.visibleRegion().boundingRect().toRectF()

  def getCenter(self) -> QPointF:
    """Getter-function for the global center"""
    return self.getViewPort().center()

  def getSideLength(self) -> float:
    """Getter-function for the length of the shortest dimension in the
    viewport."""
    return min(self.getViewPort().width(), self.getViewPort().height())

  def getOuterSquare(self) -> QRectF:
    """This method returns the largest square that would fit in the
    viewport having same center as the viewport"""
    size = QSizeF(self.getSideLength(), self.getSideLength())
    rect = QRectF(self._origin, size)
    rect.moveCenter(self.getCenter())
    return rect

  def getInnerSquare(self) -> QRectF:
    """The chessboard including and outline. Use only for painting and not
    for logic."""
    side = self.getSideLength() * (1 - 2 * self._bezelRatio)
    rect = QRectF(self._origin, QSizeF(side, side))
    rect.moveCenter(self.getCenter())
    return rect

  def getBoardRect(self) -> QRectF:
    """Getter-function for the square that exactly contains the
    chessboard."""
    inner = self.getInnerSquare()
    side = inner.width() / 2 + inner.height() / 2 - 2 * self._boardOutline
    rect = QRectF(self._origin, QSizeF(side, side))
    rect.moveCenter(self.getCenter())
    return rect

  def getSquareStep(self) -> float:
    """Getter-function for the distance between squares. This is not the
    full size of the squares as gridlines must be provided for"""
    boardRect = self.getBoardRect()
    return boardRect.height() / 16 + boardRect.width() / 16

  def getSquare(self, x: int, y: int) -> QRectF:
    """Retrieves the square at given position."""
    step = self.getSquareStep()
    boardRect = self.getBoardRect()
    left0, top0 = boardRect.left(), boardRect.top()
    right0, bottom0 = boardRect.right(), boardRect.bottom()
    left, top = left0 + x * step, top0 + y * step
    right, bottom = right0 - (7 - x) * step, bottom0 - (7 - y) * step
    leftTop, rightBottom = QPointF(left, top), QPointF(right, bottom)
    return QRectF(leftTop, rightBottom)

  def getPointSquare(self, point: QPointF) -> QRectF:
    """Getter-function for the square that would hold the given point. If
    the chessboard is not currently under the mouse an empty rectangle is
    returned."""
    boardRect = self.getBoardRect()
    x, y = point.x() - boardRect.left(), point.y() - boardRect.top()
    x, y = x / boardRect.width() * 8, y / boardRect.height() * 8
    return self.getSquare(int(x), int(y))

  def getLabelRects(self) -> dict[str, list[QRectF]]:
    """Getter-function for the bounding rectangles on the labels"""
    border = self._bezelRatio * self.getSideLength()
    boardRect, step = self.getBoardRect(), self.getSquareStep()
    step = self.getSquareStep()
    fileSize, rankSize = QSizeF(step, border), QSizeF(border, step)
    upperTop = boardRect.top() - border
    lowerTop = boardRect.bottom()
    left0, top0 = boardRect.left(), boardRect.top()
    topRects = [QRectF(QPointF(
      left0 + step * i, upperTop), fileSize) for i in range(8)]
    bottomRects = [QRectF(QPointF(
      left0 + step * i, lowerTop), fileSize) for i in range(8)]
    leftLeft = boardRect.left() - border
    rightLeft = boardRect.right()
    leftRects = [QRectF(QPointF(
      leftLeft, top0 + step * i), rankSize) for i in range(8)]
    rightRects = [QRectF(QPointF(
      rightLeft, top0 + step * i), rankSize) for i in range(8)]
    return dict(left=leftRects,
                top=topRects,
                right=rightRects,
                bottom=bottomRects)

  def getSquares(self) -> dict[str, list[QRectF]]:
    """Getter-function for all squares split according to square color"""
    light, dark, gap = [], [], self._squareGap
    for i in range(8):
      for j in range(8):
        base = self.getSquare(i, j)
        center, size = base.center(), base.size()
        newSize = QSizeF(size.width() - gap / 2, size.height() - gap / 2)
        newRect = QRectF(self._origin, newSize)
        newRect.moveCenter(center)
        if i % 2 == j % 2:
          light.append(newRect)
        else:
          dark.append(newRect)
    return dict(light=light, dark=dark)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation of paint event"""
    painter = QPainter()
    painter.begin(self)
    guessViewPort = self.getViewPort()
    self._painterViewPort.append(painter.viewport())
    backgroundStyle @ painter
    r = self._cornerRadius
    painter.drawRoundedRect(guessViewPort, r, r)
    bezelStyle @ painter
    painter.drawRoundedRect(self.getOuterSquare(), r, r)
    labelStyle @ painter
    textFlag = Qt.AlignmentFlag.AlignCenter
    files = [char for char in string.ascii_uppercase[:8]]
    ranks = reversed(['%d' % i for i in range(1, 9)])
    labels = self.getLabelRects()
    for (file, top, bottom) in zip(files, labels['top'], labels['bottom']):
      painter.drawText(top, textFlag, file)
      painter.drawText(bottom, textFlag, file)
    for (rank, left, right) in zip(ranks, labels['left'], labels['right']):
      painter.drawText(left, textFlag, rank)
      painter.drawText(right, textFlag, rank)
    outlineStyle @ painter
    painter.drawRect(self.getInnerSquare())
    gridStyle @ painter
    painter.drawRect(self.getBoardRect())
    darkSquareStyle @ painter
    lightDark = self.getSquares()
    painter.drawRects(lightDark['dark'])
    lightSquareStyle @ painter
    painter.drawRects(lightDark['light'])
    painter.end()
