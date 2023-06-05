"""PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
of pieces. It is divided into a properties class with getters and setters
as well as a main class with functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMouseEvent
from icecream import ic
from worktoy.waitaminute import UnexpectedStateError

from visualchess import MouseLayout, ChessPiece, Square

ic.configureOutput(includeContext=True)


class _PieceGrabbingProperties(MouseLayout):
  """This class provides the setters and getters for properties"""

  def __init__(self, *args, **kwargs) -> None:
    MouseLayout.__init__(self, *args, **kwargs)
    self._grabbedPiece = None
    self._originSquare = None

  #########################################################################
  ################## Accessor functions for grabbed piece #################
  #########################################################################
  def getGrabbedPiece(self) -> ChessPiece:
    """Getter-function for the currently grabbed piece."""
    if self._grabbedPiece is None:
      return ChessPiece.EMPTY
    if isinstance(self._grabbedPiece, ChessPiece):
      return self._grabbedPiece
    raise TypeError

  def setGrabbedPiece(self, piece: ChessPiece) -> NoReturn:
    """Getter-function for the currently grabbed piece."""
    if piece is None:
      self._grabbedPiece = ChessPiece.EMPTY
      return
    if isinstance(piece, ChessPiece):
      self._grabbedPiece = piece
      return
    raise TypeError

  def delGrabbedPiece(self) -> ChessPiece:
    """Deleter-function for the grabbed piece. Returns the grabbed piece."""
    piece = self.getGrabbedPiece()
    self.setGrabbedPiece(ChessPiece.EMPTY)
    return piece

  #########################################################################
  ############## END OF Accessor functions for grabbed piece ##############
  ################## Accessor functions for origin square #################
  #########################################################################
  def getOriginSquare(self) -> Square:
    """Getter-function for origin square"""
    if self._originSquare is None:
      raise UnexpectedStateError
    if isinstance(self._originSquare, Square):
      return self._originSquare
    raise TypeError

  def setOriginSquare(self, square: Square) -> NoReturn:
    """Setter-function for origin square"""
    if square is None:
      raise UnexpectedStateError
    if isinstance(square, Square):
      self._originSquare = square
    raise TypeError

  #########################################################################
  ############## END OF Accessor functions for origin square ##############
  #########################################################################


class _PieceGrabbingSignals(_PieceGrabbingProperties):
  """In between class for signal handling functions"""

  grabbedPiece = Signal(ChessPiece)
  droppedPiece = Signal(ChessPiece)
  clearSquare = Signal(Square)
  placePieceSquare = Signal(ChessPiece, Square)

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)

  def grabbedPieceFunc(self, piece: ChessPiece) -> NoReturn:
    """Handling of the piece grabbing signal"""

  def droppedPieceFunc(self, piece: ChessPiece) -> NoReturn:
    """Handling of the piece dropping signal"""

  def clearSquareFunc(self, square: Square) -> NoReturn:
    """Handling of square clearing signal"""

  def placePieceFunc(self, piece: ChessPiece, square: Square) -> NoReturn:
    """Handles the placement of piece on square signal."""


class PieceGrabbing(_PieceGrabbingSignals):
  """PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
  of pieces. It is divided into a properties class with getters and setters
  as well as a main class with functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingSignals.__init__(self, *args, **kwargs)

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse press event grabs the piece on the hovered
    square if available."""
    if event.button() == Qt.MouseButton.LeftButton:
      hoverPiece = self.getHoverPiece()
      if not hoverPiece:
        return
      self.grabbedPiece.emit(hoverPiece)

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse release event which releases the item
    either on the hovered square if allowed or back at origin square."""
    if event.button() == Qt.MouseButton.LeftButton:
      grabbedPiece = self.getGrabbedPiece()
      if grabbedPiece:
        self.droppedPiece.emit(self.getGrabbedPiece())
