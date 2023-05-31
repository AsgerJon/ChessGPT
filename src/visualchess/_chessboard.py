"""The chessBoard function creates appropriate rectangles for the chess
board given a specific size"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from icecream import ic

from worktoy.waitaminute import ProceduralError

if TYPE_CHECKING:
  from typing import Any
else:
  from worktoy.typetools import Any

from PySide6.QtCore import QSizeF, QSize, QRectF, QPointF
from worktoy.field import BaseField
from worktoy.typetools import TypeBag

Squares = tuple[list[QRectF], list[QRectF]]
Size = TypeBag(QSize, QSizeF)

ic.configureOutput(includeContext=True)


@BaseField('boardSizeRatio', 1 - 32 / 400, type_=float)
@BaseField('bezelRatio', 32 / 400, type_=float)
@BaseField('gridRatio', 8 / 400, type_=float)
class ChessBoard:
  """The chessBoard function creates appropriate rectangles for the chess
  board given a specific size
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def _getOrigin() -> QPointF:
    """Getter-function for the origin"""
    return QPointF(0., 0.)

  def __init__(self, *args, **kwargs) -> None:
    self._globalRect = None

  def __call__(self, globalSize: QSizeF) -> Any:
    """Updates the rectangles"""
    self._globalRect = globalSize

  def _getGlobalRect(self) -> QRectF:
    """Getter-function for the global rectangle"""
    return self._globalRect

  def _getGlobalCenter(self) -> QPointF:
    """Getter-function for the global center"""
    return self._getGlobalRect().center()

  def _getGlobalSize(self) -> QSizeF:
    """Getter-function for the global size"""
    return self._getGlobalRect().size()

  def _getBezelRect(self) -> QRectF:
    """Getter-function for the bezel rectangle"""
    height, = self._getGlobalRect().height()
    width, = self._getGlobalRect().width()
    bezelSize = QSizeF(min([height, width]), min([height, width]))
    bezelSquare = QRectF(self._getOrigin(), bezelSize)
    bezelSquare.moveCenter(self._getGlobalCenter())
    return bezelSquare

  def _getBezelSize(self) -> QSizeF:
    """Getter-function for the size of the bezel"""
    return self._getBezelRect().size()

  def _getBezelHeight(self) -> float:
    """Getter-function for height of the bezel rectangle"""
    return self._getBezelRect().height()

  def _getBezelWidth(self) -> float:
    """Getter-function for width of the bezel rectangle"""
    return self._getBezelRect().width()

  def _getBezelTopLeft(self) -> QPointF:
    """Getter-function for the top left corner of the bezel"""
    return self._getBezelRect().topLeft()

  def _getBoardRect(self) -> QRectF:
    """Getter-function for the board rectangle"""
    ratio = self.boardSizeRatio
    width = self._getBezelWidth()
    height = self._getBezelHeight()
    size = QSizeF(*[ratio * i for i in [width, height]], )
    rect = QRectF(self._getOrigin(), size)
    rect.moveCenter(self._getGlobalCenter())
    return rect

  def _getBoardSize(self) -> QSizeF:
    """Getter-function for the board size"""
    return self._getBoardRect().size()

  def _getBoardWidth(self) -> float:
    """Getter-function for the board width"""
    return self._getBoardSize().width()

  def _getBoardHeight(self) -> float:
    """Getter-function for the board height"""
    return self._getBoardSize().height()

  def _getBoardLeft(self) -> float:
    """Getter-function for the left side of the board"""
    return self._getBoardRect().left()

  def _getBoardTop(self) -> float:
    """Getter-function for the top side of the board"""
    return self._getBoardRect().right()

  def _getSquareSize(self) -> QSizeF:
    """Getter-function for square size"""
    width = self._getBoardWidth() * (1 - self.gridRadio)
    height = self._getBoardHeight() * (1 - self.gridRadio)
    return QSizeF(width / 8, height / 8)

  def _getSquareStep(self) -> float:
    """Getter-function for the step for the squares. This is the side
    length of the squares, but without the grids subtracted."""
    width = self._getBoardWidth()
    height = self._getBoardHeight()
    if (width - height) ** 2 > 4:
      raise ProceduralError('width and height not equal')
    return (width + height) / 2

  def _collectedSquares(self, ) -> Squares:
    """Collecting the squares """
    light, dark = [], []
    left0, top0 = self._getBoardLeft(), self._getBoardTop()
    step, size = self._getSquareStep(), self._getSquareSize()
    for i in range(8):
      for j in range(8):
        left, top = left0 + step * i, top0 + step * j
        rect = QRectF(QPointF(left, top), size)
        if i % 2 == j % 2:
          light.append(rect)
        else:
          dark.append(rect)
    return (light, dark)
