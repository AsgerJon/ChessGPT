"""PaintBoard paints the board on a paint device"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Any, Never

from PySide6.QtCore import QRectF, QSizeF, QPointF, QRect
from PySide6.QtGui import QPaintEvent, QPaintDevice
from icecream import ic
from worktoy.parsing import maybeType
from worktoy.typetools import CallMeMaybe, TypeBag
from worktoy.waitaminute import ProceduralError, ReadOnlyError

from workstyle.styles import BezelStyle, GridStyle, LightSquareStyle, \
  DarkSquareStyle

Squares = tuple[list[QRectF], list[QRectF]]
Rect = TypeBag(QRectF, QRect)

ic.configureOutput(includeContext=True)


class PaintBoard:
  """PaintBoard paints the board on a paint device
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  origin = QPointF(0., 0.)

  _paintStyles = {
    'bezel': BezelStyle,
    'grid': GridStyle,
    'light': LightSquareStyle,
    'dark': DarkSquareStyle
  }

  @classmethod
  def getPaintStyles(cls, ) -> dict:
    """Creates an instance fitting the given paint event"""
    return cls._paintStyles

  def __init__(self, ) -> None:
    self._outerRectangle = None
    self._gridRatio = 6.25e-03
    self._bezelRatio = 40e-03
    self._boardSizeRatio = 1 - self._bezelRatio
    self.__content__ = None

  def __call__(self, cls) -> type:
    """Decorates a paint event"""
    setattr(cls, 'paintBoard', self)
    setattr(cls, 'fitBoard', self.fitInRect)
    setattr(cls, 'paintStyles', self.getPaintStyles())
    return cls

  def fitInRect(self, rect: Rect) -> NoReturn:
    """Fits this instance in given rectangle"""
    if isinstance(rect, QRect):
      return self.fitInRect(rect.toRectF())
    self._outerRectangle = rect
    self._resetContent()
    self._createContent()

  def getBezelRatio(self) -> float:
    """Getter-function for bezel ratio"""
    return self._bezelRatio

  def getOuterRectangle(self) -> QRectF:
    """Getter-function for the outer rectangle."""
    if self._outerRectangle is None:
      raise ProceduralError()
    if isinstance(self._outerRectangle, QRectF):
      return self._outerRectangle

  def getCenter(self) -> QPointF:
    """Getter-function for the global center"""
    return self.getOuterRectangle().center()

  def getSize(self) -> QSizeF:
    """Getter-function for the global size"""
    return self.getOuterRectangle().size()

  def getBaseRect(self) -> QRectF:
    """Getter-function for background rectangle. The borders around the
    board will remain on this rectangle."""
    outerSize = self.getOuterRectangle().size()
    baseSide = min(outerSize.width(), outerSize.height())
    baseSquare = QRectF(PaintBoard.origin, QSizeF(baseSide, baseSide))
    baseSquare.moveCenter(self.getOuterRectangle().center())
    return baseSquare

  def getBaseSize(self) -> QSizeF:
    """Getter-function for base size"""
    return self.getBaseRect().size()

  def getBoardRect(self) -> QRectF:
    """Getter-function for the board rectangle containing the squares
    inside the bezels"""
    size = self.getBaseSize() * self.getBezelRatio()
    boardRect = QRectF(self.origin, size)
    boardRect.moveCenter(self.getCenter())
    return boardRect

  def getBoardSize(self) -> QSizeF:
    """Getter-function for board size"""
    return self.getBoardRect().size()

  def getBoardTopLeft(self) -> QPointF:
    """Getter-function for top left"""
    return self.getBoardRect().topLeft()

  def squareSize(self) -> QSizeF:
    """Getter-function for the square size"""
    return (self.getBoardSize() * (1 - self._gridRatio)) / 8

  def squareStep(self) -> float:
    """Getter-function for the step size"""
    return (self.getBoardSize().width() + self.getBoardSize().width()) / 16

  def collectSquares(self) -> Squares:
    """Collects the squares"""
    topLeft, size = self.getBoardTopLeft(), self.squareSize()
    top, left, light, dark, = topLeft.x(), topLeft.y(), [], []
    step = self.squareStep()
    for i in range(8):
      for j in range(8):
        topLeft = QPointF(left + i * step, top + j * step)
        square = QRectF(topLeft, size)
        if i % 2 == j % 2:
          light.append(square)
        else:
          dark.append(square)
    return (light, dark)

  def _resetContent(self) -> NoReturn:
    """Resets the current content. This is required when applying to a
    different size."""
    self.__content__ = None

  def _createContent(self) -> NoReturn:
    """Creator function for content"""
    bezel = self.getBaseRect()
    grid = self.getBoardRect()
    light, dark = self.collectSquares()
    self.__content__ = {
      'bezel': bezel,
      'grid': grid,
      'light': light,
      'dark': dark
    }

  def _getContent(self) -> dict:
    """Getter-function for contents"""
    if self.__content__ is None:
      self._createContent()
      return self._getContent()
    return self.__content__

  def __getitem__(self, key: str) -> Any:
    """Dictionary operations"""
    out = self._getContent().get(key, None)
    if out is None:
      raise KeyError(key)

  def __setitem__(self, key: str, *_) -> Never:
    """Illegal setter"""
    raise ReadOnlyError(key)

  def __delitem__(self, key: str, ) -> Never:
    """Illegal setter"""
    raise ReadOnlyError(key)
