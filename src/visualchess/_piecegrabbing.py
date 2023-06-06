"""PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
of pieces. It is divided into a properties class with getters and setters
as well as a main class with functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Signal, Qt, Slot
from PySide6.QtGui import QMouseEvent
from icecream import ic
from worktoy.waitaminute import UnexpectedStateError

from visualchess import MouseLayout, ChessPiece, Square, SoundBoard, Sound

ic.configureOutput(includeContext=True)


class _PieceGrabbingProperties(MouseLayout):
  """This class provides the setters and getters for properties"""

  def __init__(self, *args, **kwargs) -> None:
    MouseLayout.__init__(self, *args, **kwargs)
    self._grabbedPiece = None
    self._originSquare = None
    self._normalCursor = Qt.CursorShape.ArrowCursor
    self._hoverCursor = Qt.CursorShape.OpenHandCursor
    self._grabCursor = Qt.CursorShape.ClosedHandCursor

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
  def getOriginSquare(self) -> Square | bool:
    """Getter-function for origin square"""
    if self._originSquare is None:
      return False
    if isinstance(self._originSquare, Square):
      return self._originSquare
    raise TypeError

  def setOriginSquare(self, square: Square) -> NoReturn:
    """Setter-function for origin square"""
    if square is None:
      raise UnexpectedStateError
    if isinstance(square, Square):
      self._originSquare = square
      return
    raise TypeError

  #########################################################################
  ############## END OF Accessor functions for origin square ##############
  #########################################################################


class _PieceGrabbingSignals(_PieceGrabbingProperties):
  """In between class for signal handling functions"""

  alertGrabbedPiece = Signal(ChessPiece)
  alertDroppedPiece = Signal(ChessPiece)
  alertClearedSquare = Signal(Square)
  alertPiecePlaced = Signal(ChessPiece, Square)

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)


class PieceGrabbing(_PieceGrabbingSignals):
  """PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
  of pieces. It is divided into a properties class with getters and setters
  as well as a main class with functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingSignals.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self.alertGrabbedPiece.connect(self.handleGrabbedPiece)
    self.alertDroppedPiece.connect(self.handleDroppedPiece)
    self.alertClearedSquare.connect(self.handleClearedSquare)
    self.alertPiecePlaced.connect(self.handlePiecePlaced)

  #########################################################################
  ####################### Signal Handling Functions #######################
  #########################################################################
  def handleGrabbedPiece(self, piece: ChessPiece) -> NoReturn:
    """Handles the piece grabbing signal"""
    self.setGrabbedPiece(piece)
    square = self.getHoverSquare()
    self.setOriginSquare(square)
    self.delHoverPiece()
    self.setPieceCursor(piece)
    self.getBoardState().setPiece(square, ChessPiece.EMPTY)

  def handleDroppedPiece(self, piece: ChessPiece) -> NoReturn:
    """Handles the piece dropping signal"""

  def handleClearedSquare(self, square: Square) -> NoReturn:
    """Handles clear square signal"""

  def handlePiecePlaced(self, piece: ChessPiece, square: Square) -> NoReturn:
    """Handles piece placed signal"""
    Sound.MOVE.play()
    self.getBoardState().setPiece(square, piece)
    if self.getBoardState().getPiece(square) == piece:
      self.delGrabbedPiece()

  #########################################################################
  ########################## Mouse button events ##########################

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse press event grabs the piece on the hovered
    square if available."""
    if event.button() == Qt.MouseButton.LeftButton:
      hoverPiece = self.getHoverPiece()
      if not hoverPiece:
        return
      self.alertGrabbedPiece.emit(hoverPiece)

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse release event which releases the item
    either on the hovered square if allowed or back at origin square."""
    if event.button() == Qt.MouseButton.LeftButton:
      grabbedPiece = self.getGrabbedPiece()
      hoverSquare = self.getHoverSquare()
      originSquare = self.getOriginSquare()
      if not originSquare:
        return
      if grabbedPiece:
        if hoverSquare:
          self.alertPiecePlaced.emit(grabbedPiece, hoverSquare)
        elif originSquare:
          self.alertPiecePlaced.emit(grabbedPiece, originSquare)
        else:
          raise UnexpectedStateError
      self.setHoverSquare(hoverSquare)
      self.setHoverPiece(grabbedPiece)
      self.setHoverCursor()

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """The mouse layout subclass brings the hover functionality."""
    if not self.getBoardRect().contains(event.position()):
      return self.delHoverSquare() or self.delHoverPiece()

    square = Square.fromPointRect(event.position(), self.getBoardRect())
    self.setHoverSquare(square)
    if self.getGrabbedPiece():
      return
    hoverPiece = self.getBoardState().getPiece(square)
    if not hoverPiece:
      if self.getHoverPiece():
        return self.delHoverPiece()
      return
    if self.getHoverPiece() == hoverPiece:
      return
    self.setHoverPiece(hoverPiece)
  #########################################################################
