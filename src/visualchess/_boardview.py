"""BoardView provides the painter width commands to draw the chess board"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic
from PySide6.QtCore import QSize, QPointF, QSizeF, QRectF, Qt, QRect
from PySide6.QtGui import QPainter, QPaintDevice
from worktoy.core import maybe
from worktoy.parsing import maybeType
from worktoy.typetools import CallMeMaybe, TypeBag
from worktoy.waitaminute import UnexpectedStateError

from visualchess import File, Rank
from workstyle.shapesettings import ShapeSettings
from workstyle.stylesettings import backgroundStyle, bezelStyle, \
  outlineStyle, gridStyle, darkSquareStyle, lightSquareStyle, \
  hoveredSquareStyle, labelStyle

ic.configureOutput(includeContext=True)

Size = TypeBag(QSize, QSizeF)


class BoardView:
  """Board Dimension on a Dynamic Viewport"""

  @staticmethod
  def getBezels() -> int:
    """Getter-function for the pixels that should be assigned to a board
    of given size."""
    return ShapeSettings.bezelWidth()

  @staticmethod
  def getInnerGrid() -> int:
    """Getter-function for the pixel width of the gridlines"""
    return ShapeSettings.squareGap()

  @staticmethod
  def getOuterGrid() -> int:
    """Getter-function for the pixel width of line around the squares"""
    return ShapeSettings.borderOutline()

  _origin = QPointF(0, 0)

  def __init__(self, device: QPaintDevice) -> None:
    self._device = device
    self._viewWidth = 400
    self._viewHeight = 400
    self._hoverSquare = None
    self._file = None
    self._rank = None
    self._slots = []
    self._shapeSettings = ShapeSettings()

  def setViewSize(self, viewSize: Size) -> NoReturn:
    """Setter-function for the view port"""
    if isinstance(viewSize, QRect):
      viewSize = viewSize.toRectF()
    self._shapeSettings.setViewPort(QRectF(QPointF(0, 0), viewSize))

  def clearHoverSquare(self, ) -> NoReturn:
    """Deleter-function for the hover square"""
    self._hoverSquare = QRectF()

  def setHoverSquare(self, *args) -> NoReturn:
    """Setter-function for the hover square"""
    file = maybeType(File, *args)
    rank = maybeType(Rank, *args)
    if isinstance(file, File) and isinstance(rank, Rank):
      self._file, self._rank = file, rank
      self._hoverSquare = self.getSquareRect(file, rank)
      self._update()

  def _update(self) -> NoReturn:
    """Updates listeners"""
    for slot in self._slots:
      slot()

  def onUpdate(self, slot: CallMeMaybe) -> NoReturn:
    """Adds slot to list of slots to be notified by updates."""
    self._slots.append(slot)

  def getHoverSquare(self) -> QRectF:
    """Getter-function for the hovered square"""
    if self._hoverSquare is None:
      self.clearHoverSquare()
    return self._hoverSquare

  def __call__(self, painter: QPainter) -> NoReturn:
    """Applies to painter"""
    self.setSize(painter.viewport().size())

    backgroundStyle @ painter
    painter.drawRect(self.outer())
    bezelStyle @ painter
    painter.drawRect(self.inner())
    labelStyle @ painter
    textFlag = Qt.AlignmentFlag.AlignCenter
    for label in [*[f for f in File], *[r for r in Rank]]:
      if isinstance(label, File):
        rects = self.getFileLabelRects(label)
      elif isinstance(label, Rank):
        rects = self.getRankLabelRects(label)
      else:
        raise UnexpectedStateError()
      for rect in rects:
        textRect = painter.boundingRect(rect, textFlag, '%s' % label)
        if isinstance(textRect, QRect):
          textRect = textRect.toRectF()
        targetSize = QSizeF(textRect.width() * 0.9,
                            textRect.height() * 0.9)
        targetRect = QRectF(QPointF(0, 0), targetSize)
        targetRect.moveCenter(textRect.center())
        painter.drawText(targetRect, textFlag, '%s' % label)
    outlineStyle @ painter
    painter.drawRect(self.getBoardOutline())
    gridStyle @ painter
    painter.drawRect(self.getBoardRect())
    darkSquareStyle @ painter
    painter.drawRects(self.getDarkSquares())
    lightSquareStyle @ painter
    painter.drawRects(self.getLightSquares())
    hoverSquare = self.getHoverSquare()
    if hoverSquare is not None:
      hoveredSquareStyle @ painter
      painter.drawRect(self.getHoverSquare())

  def setSize(self, size: QSize) -> NoReturn:
    """Setter-function for the size"""
    self._viewWidth = size.width()
    self._viewHeight = size.height()

  def sideLength(self) -> int:
    """Getter-function for the shortest side"""
    width, height = self._viewWidth, self._viewHeight
    return width if width < height else height

  def viewSize(self, ) -> QSizeF:
    """Setter-function for viewport"""
    return QSizeF(self._viewWidth, self._viewHeight)

  def outer(self) -> QRectF:
    """The outer boundaries of the viewport. """
    return QRectF(QPointF(0, 0), self.viewSize())

  def center(self) -> QPointF:
    """Getter function for the global center"""
    return QPointF(self._viewWidth / 2, self._viewHeight / 2)

  def inner(self) -> QRectF:
    """The largest square fitting in the viewport. This is the size of
    board including the bezels."""
    side = self.sideLength()
    rect = QRectF(self._origin, QSizeF(side, side))
    rect.moveCenter(self.center())
    return rect

  def getBoardOutline(self) -> QRectF:
    """The QRectF whose outline is the borderline"""
    side = self.sideLength() - 2 * self.getBezels()
    out = QRectF(self._origin, QSize(side, side))
    out.moveCenter(self.center())
    return out

  def getBoardRect(self) -> QRectF:
    """The QRectF that will be covered entirely by light and dark squares.
    It does not include the thin borderline around the board."""
    sideLength = self.sideLength()
    bezels = 2 * self.getBezels()
    border = 2 * ShapeSettings.borderOutline()
    side = sideLength - bezels - border
    loss = (side - self.getInnerGrid() * 7) % 8
    out = QRectF(self._origin, QSize(side + 8 - loss, side + 8 - loss))
    out.moveCenter(self.center())
    return out

  def getSquareSize(self) -> int:
    """Getter-function for the size of each square"""
    width = self.getBoardRect().width()
    height = self.getBoardRect().height()
    side = width / 2 + height / 2
    return (side - 7 * self.getInnerGrid()) / 8

  def getLeft0(self) -> int:
    """Getter-function for the left boundary of the board rectangle."""
    return self.getBoardRect().left()

  def getTop0(self) -> int:
    """Getter-function for the top boundary of the board rectangle."""
    return self.getBoardRect().top()

  def getSquareStep(self) -> int:
    """Getter-function for the distance between left sides of two
    consecutive squares."""
    board = self.getBoardRect()
    return board.width() / 16 + board.height() / 16

  def getSquareRect(self, file: File, rank: Rank, ) -> QRectF:
    """Getter-function for the rectangle at given file and rank"""
    board = self.getBoardRect()
    boardWidth, boardHeight = board.width(), board.height()
    boardLeft, boardTop = board.left(), board.top()
    boardRight, boardBottom = board.right(), board.bottom()
    left = boardLeft + file.value * boardWidth / 8
    top = boardTop + rank.value * boardHeight / 8
    right = boardRight - (7 - file.value) * boardWidth / 8
    bottom = boardBottom - (7 - rank.value) * boardHeight / 8
    left += self.getInnerGrid() / 2
    top += self.getInnerGrid() / 2
    right -= self.getInnerGrid() / 2
    bottom -= self.getInnerGrid() / 2
    return QRectF(QPointF(left, top), QPointF(right, bottom))

  def getSquaresIf(self, condition: CallMeMaybe = None) -> list[QRectF]:
    """Getter-function for squares given a condition"""
    out = []
    condition = maybe(condition, lambda f, r: True)
    for (i, file) in enumerate(File):
      for (j, rank) in enumerate(Rank):
        if condition(file, rank):
          out.append(self.getSquareRect(file, rank))
    return out

  def getLightSquares(self) -> list[QRectF]:
    """Getter-function for list of rectangles on the light squares"""
    out = []
    for (i, file) in enumerate(File):
      for (j, rank) in enumerate(Rank):
        if i % 2 == j % 2:
          out.append(self.getSquareRect(file, rank))
    return out

  def getDarkSquares(self) -> list[QRectF]:
    """Getter-function for list of rectangles on the dark squares"""
    out = []
    for (i, file) in enumerate(File):
      for (j, rank) in enumerate(Rank):
        if i % 2 != j % 2:
          out.append(self.getSquareRect(file, rank))
    return out

  def getSquarePoint(self, point: QPointF) -> QRectF:
    """Identifies the square containing the point given"""

    def func(file: File, rank: Rank) -> bool:
      """Point in rectangle"""
      left0, top0 = self.getLeft0(), self.getTop0()
      step = self.getSquareStep()
      x, y = point.x(), point.y()
      left, right = [left0 + step * (file.value + i) for i in [0, 1]]
      top, bottom = [top0 + step * (rank.value + i) for i in [0, 1]]
      if x < left or right < x or y < top or bottom < y:
        return False
      return True

    return [*self.getSquaresIf(func), QRectF()][0]

  def getFileLabelRects(self, file: File) -> list[QRectF]:
    """Getter-function for the rectangle for the labels on given file"""
    width = self.getSquareStep()
    left = self.getLeft0() + file.value * width
    height = self.getBezels()
    size = QSizeF(width, height)
    upperTop = self.getTop0() - height - self.getOuterGrid()
    bottom0 = self.getBoardRect().bottom()
    lowerTop = bottom0 + self.getOuterGrid()
    upperRect = QRectF(QPointF(left, upperTop), size)
    lowerRect = QRectF(QPointF(left, lowerTop), size)
    return [upperRect, lowerRect]

  def getRankLabelRects(self, rank: Rank) -> list[QRectF]:
    """Getter-function for the rectangle for the labels on given rank"""
    width, height = self.getBezels(), self.getSquareStep()
    size = QSizeF(width, height)
    leftLeft = self.getBoardRect().left() - self.getOuterGrid() - width
    rightLeft = self.getBoardRect().right() + self.getOuterGrid()
    top = self.getBoardRect().top() + height * rank.value
    leftRect = QRectF(QPointF(leftLeft, top), size)
    rightRect = QRectF(QPointF(rightLeft, top), size)
    return [leftRect, rightRect]
