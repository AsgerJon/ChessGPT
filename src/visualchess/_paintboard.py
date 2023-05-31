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

from workstyle import WhereMouse
from workstyle.styles import BezelStyle, GridStyle, LightSquareStyle, \
  DarkSquareStyle

Squares = tuple[list[QRectF], list[QRectF]]
Rect = TypeBag(QRectF, QRect)

ic.configureOutput(includeContext=True)


class PaintBoard(WhereMouse):
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

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)
    self._outerRectangle = QSizeF(256, 256)
    self._gridRatio = 8 / 400
    self._bezelRatio = 32 / 400
    self._boardSizeRatio = 1 - self._bezelRatio
    self.__content__ = None
    self._globalCenter = None
    self._globalSize = None
    self._boardSize = None
    self._boardHeight = None
    self._boardWidth = None
    self._boardRect = None
    self._squareSize = None
    self._squareStep = None
    self._bezelSquare = None

  def getBoardSizeRatio(self) -> float:
    """Getter-function for the board size ratio"""
    return self._boardSizeRatio

  def getOuterRectangle(self) -> QRectF:
    """Getter-function for the outer rectangle."""
    if self._outerRectangle is None:
      raise ProceduralError()
    if isinstance(self._outerRectangle, QRectF):
      return self._outerRectangle

  def getGlobalSize(self) -> QSizeF:
    """Getter-function for outer rectangle"""
    if self._outerRectangle is None:
      raise ProceduralError()
    if self._globalSize is None:
      self._globalSize = self._outerRectangle.size()
    return self._globalSize

  def getGlobalCenter(self) -> QPointF:
    """Getter-function for outer center"""
    if self._outerRectangle is None:
      raise ProceduralError()
    if self._globalCenter is None:
      self._globalCenter = self._outerRectangle.center()
    return self._globalCenter

  def getBezelSquare(self) -> QRectF:
    """Getter-function for background rectangle. The borders around the
    board will remain on this rectangle."""
    bezelSide = min(self._globalSize.height(), self._globalSize.width())
    bezelSquare = QRectF(PaintBoard.origin, QSizeF(bezelSide, bezelSide))
    bezelSquare.moveCenter(self._globalCenter)
    self._bezelSquare = bezelSquare
    return self._bezelSquare

  def getBoardHeight(self) -> float:
    """Getter-function for board height"""
    ratio = self.getBoardSizeRatio()
    self._boardHeight = self._bezelSquare.height() * ratio
    return self._boardHeight

  def getBoardWidth(self) -> float:
    """Getter-function for board width"""
    ratio = self.getBoardSizeRatio()
    self._boardWidth = self._bezelSquare.width() * ratio
    return self._boardWidth

  def getBoardSize(self) -> QSizeF:
    """Getter-function for board size"""
    self._boardSize = QSizeF(self._boardHeight, self._boardWidth)

  def getBoardRect(self) -> QRectF:
    """Getter-function for the board rectangle containing the squares
    inside the bezels"""
    ratio = self.getBoardSizeRatio()
    self._boardHeight = self._bezelSquare.height() * ratio
    self._boardWidth = self._bezelSquare.width() * ratio
    self._boardSize = QSizeF(self._boardWidth, self._boardHeight)
    self._boardRect = QRectF(PaintBoard.origin, self._boardSize)
    return self._boardRect

  def getBoardTopLeft(self) -> QPointF:
    """Getter-function for top left"""
    return self.getBoardRect().topLeft()

  def squareSize(self) -> QSizeF:
    """Getter-function for the square size"""
    return (self.getBoardSize() * (1 - self._gridRatio)) / 8

  def squareStep(self) -> float:
    """Getter-function for the step size"""
    return (self.getBoardSize().width() + self.getBoardSize().height()) / 16

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
