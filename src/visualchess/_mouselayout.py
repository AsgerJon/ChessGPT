"""MouseLayout"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter
from icecream import ic

from visualchess import PieceLayout, ChessPiece, Square
from workstyle.stylesettings import hoveredSquareStyle

ic.configureOutput(includeContext=True)


class _MouseLayoutProperties(PieceLayout):
  """Class containing properties"""

  changedHoverSquare = Signal(Square)
  clearedHoverSquare = Signal()
  changedHoverPiece = Signal(ChessPiece)
  clearedHoverPiece = Signal()

  def __init__(self, *args, **kwargs) -> None:
    PieceLayout.__init__(self, *args, **kwargs)
    self._hoverSquare = None
    self._hoverPiece = None

  #########################################################################
  ######################### Hover square accessors ########################
  #########################################################################
  def getHoverSquare(self) -> Square:
    """Getter-function for hovered rectangle"""
    return self._hoverSquare

  def setHoverSquare(self, square: Square) -> NoReturn:
    """Setter-function for hovered rectangle"""
    if self._hoverSquare == square:
      return
    self.changedHoverSquare.emit(square)
    self._hoverSquare = square

  def clearHoverSquare(self) -> NoReturn:
    """Deleter-function for the hovered rectangle"""
    if self._hoverSquare:
      self._hoverSquare = None
      self.clearedHoverSquare.emit()

  #########################################################################
  ##################### END of Hover square accessors #####################
  ######################### Hover piece Accessors #########################
  #########################################################################
  def getHoverPiece(self) -> object:
    """Getter-function for hover piece"""
    return self._hoverPiece

  def setHoverPiece(self, hoverPiece: ChessPiece) -> NoReturn:
    """Setter-function for hover piece"""
    if hoverPiece == self._hoverPiece:
      return
    self._hoverPiece = hoverPiece
    self.changedHoverPiece.emit(hoverPiece)

  def clearHoverPiece(self) -> NoReturn:
    """Deleter-function for hover piece"""
    if self._hoverPiece:
      self._hoverPiece = None
      self.clearedHoverPiece.emit()

  #########################################################################
  ###################### END of Hover piece accessors #####################
  #########################################################################
  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation. At this stage the hovered rectangle is highlighted."""
    PieceLayout.paintEvent(self, event)


class MouseLayout(_MouseLayoutProperties):
  """The mouse layout subclass of piece layout brings mouse functionality."""

  def __init__(self, *args, **kwargs) -> None:
    _MouseLayoutProperties.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self.changedHoverSquare.connect(self.changedHoverSquareFunc)
    self.clearedHoverSquare.connect(self.clearedHoverSquareFunc)
    self.changedHoverPiece.connect(self.changedHoverPieceFunc)
    self.clearedHoverPiece.connect(self.clearedHoverPieceFunc)

  def changedHoverSquareFunc(self, square: Square) -> NoReturn:
    """Handles changes to hover square"""
    self.update()

  def clearedHoverSquareFunc(self) -> NoReturn:
    """Handles the clearing of the hover square"""
    self.update()

  def changedHoverPieceFunc(self, piece: ChessPiece) -> NoReturn:
    """Handles changes to the piece being hovered"""
    self.setCursor(Qt.CursorShape.OpenHandCursor)
    self.update()

  def clearedHoverPieceFunc(self) -> NoReturn:
    """Clears the hover piece func"""
    self.setCursor(Qt.CursorShape.ArrowCursor)
    self.update()

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementing mouse move event"""
    if not self.getBoardRect().contains(event.position()):
      return self.clearHoverSquare()
    square = Square.fromPointRect(event.position(), self.getBoardRect())
    self.setHoverSquare(square)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation. At this stage the hovered rectangle is highlighted."""
    _MouseLayoutProperties.paintEvent(self, event)
    if self.getHoverSquare() is None:
      return
    painter = QPainter()
    painter.begin(self)
    hoveredSquareStyle @ painter
    painter.drawRect(self.getHoverSquare() @ self.getBoardRect())
    painter.end()

  def hoverPiece(self, square: int, ) -> NoReturn:
    """Method responsible for handling piece hovering"""

  def grabPiece(self, square: int, ) -> NoReturn:
    """Method responsible for handling piece grabbing"""
