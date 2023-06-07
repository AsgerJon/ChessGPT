"""BoardMouse is a subclass of BoardWidget that provides the mouse related
logic."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string
from typing import NoReturn

from PySide6.QtCore import Qt, QPointF, QRectF, QSizeF
from PySide6.QtGui import QPaintEvent, QPainter, QCursor
from icecream import ic

from visualchess import Square, ChessPiece, Settings
from workstyle import CoreWidget
from workstyle.stylesettings import backgroundStyle, bezelStyle, \
  labelStyle, outlineStyle, gridStyle, darkSquareStyle, lightSquareStyle

ic.configureOutput(includeContext=True)


class BoardLayout(CoreWidget):
  """This class provides the size relating functions and settings."""

  #########################################################################
  ############################ Static Settings ############################
  _bezelRatio = Settings.bezelRatio
  _squareGap = Settings.squareGap
  _boardOutline = Settings.boardOutline
  _cornerRadius = Settings.cornerRadius
  _adjustFontSize = Settings.adjustFontSize
  _origin = Settings.origin
  _normalCursor = Settings.normalCursor
  _hoverCursor = Settings.hoverCursor
  _grabCursor = Settings.grabCursor
  _deviceName = Settings.deviceName

  ######################### END OF Static Settings ########################
  # --------------------------------------------------------------------- #
  ############## Accessor Functions for Instances of QCursor ##############
  @classmethod
  def getNormalCursorShape(cls) -> Qt.CursorShape:
    """Getter function for normal cursor"""
    if isinstance(cls._normalCursor, Qt.CursorShape):
      return cls._normalCursor
    raise TypeError

  @classmethod
  def getNormalCursor(cls, ) -> QCursor:
    """Getter-function for normal cursor"""
    cursor = QCursor()
    cursor.setShape(cls.getNormalCursorShape())
    if isinstance(cursor, QCursor):
      return cursor
    raise TypeError

  @classmethod
  def getHoverCursorShape(cls) -> Qt.CursorShape:
    """Getter function for hover cursor"""
    if isinstance(cls._hoverCursor, Qt.CursorShape):
      return cls._hoverCursor
    raise TypeError

  @classmethod
  def getHoverCursor(cls, ) -> QCursor:
    """Getter-function for hover cursor"""
    cursor = QCursor()
    cursor.setShape(cls.getHoverCursorShape())
    if isinstance(cursor, QCursor):
      return cursor
    raise TypeError

  @classmethod
  def getGrabCursorShape(cls) -> Qt.CursorShape:
    """Getter function for grab cursor"""
    if isinstance(cls._grabCursor, Qt.CursorShape):
      return cls._grabCursor
    raise TypeError

  @classmethod
  def getGrabCursor(cls, ) -> QCursor:
    """Getter-function for grab cursor"""
    cursor = QCursor()
    cursor.setShape(cls.getGrabCursorShape())
    if isinstance(cursor, QCursor):
      return cursor
    raise TypeError

  ########### END OF Accessor Functions for Instances of QCursor ##########
  # --------------------------------------------------------------------- #
  #########################################################################
  #########################################################################
  ###################### Instance Setters for Cursor ######################

  def setNormalCursor(self) -> NoReturn:
    """Sets the cursor on the widget to normal shape"""
    self.setCursor(self.getNormalCursor())

  def setHoverCursor(self, ) -> NoReturn:
    """Sets the cursor on the widget to hover shape. This should be an
    open hand to indicate the availability to grab the item being hovered."""
    self.setCursor(self.getHoverCursor())

  def setGrabCursor(self, ) -> NoReturn:
    """Sets the cursor on the widget to grabbing shape. This should be
    indicated on top of the chess piece being grabbed if possible rather
    than invoking this function."""
    self.setCursor(self.getGrabCursor())

  def setPieceCursor(self, piece: ChessPiece) -> NoReturn:
    """Sets the cursor on the widget to grab the given piece."""
    self.setCursor(piece.getCursor())

  ################### END OF Instance Setters for Cursor ##################
  #########################################################################
  def getViewPort(self) -> QRectF:
    """This method predicts the viewport on the widget"""
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

  def getLabelRects(self) -> dict[str, list[QRectF]]:
    """Getter-function for the bounding rectangles on the labels"""
    border = self._bezelRatio * self.getSideLength()
    boardRect, step = self.getBoardRect(), self.getSquareStep()
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
        square = Square.fromInts(i, j)
        base = square @ self.getBoardRect()
        if isinstance(base, QRectF):
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
    """The BoardLayout subclass draws the static elements of the
    chessboard"""
    painter = QPainter()
    painter.begin(self)
    guessViewPort = self.getViewPort()
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
    gridStyle @ painter
    painter.drawRect(self.getBoardRect())
    darkSquareStyle @ painter
    lightDark = self.getSquares()
    painter.drawRects(lightDark['dark'])
    lightSquareStyle @ painter
    painter.drawRects(lightDark['light'])
    outlineStyle @ painter
    painter.drawRect(self.getInnerSquare())
    painter.end()
