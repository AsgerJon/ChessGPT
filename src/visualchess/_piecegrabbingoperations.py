"""The '_PieceGrabbingOperations' class defines the operations used by the
PieceGrabbing widget."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn
from warnings import warn

from PySide6.QtCore import QEvent
from PySide6.QtGui import QMouseEvent
from icecream import ic
from worktoy.core import plenty
from worktoy.waitaminute import ProceduralError

from visualchess import _PieceGrabbingProperties, ChessPiece, Sound, \
  Square, \
  Settings

ic.configureOutput(includeContext=True)


class _PieceGrabbingOperations(_PieceGrabbingProperties):
  """The '_PieceGrabbingOperations' class defines the operations used by the
  PieceGrabbing widget.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)
    self._cancelGrabbingOperation = None

  def leaveBoardRect(self, event: QEvent) -> NoReturn:
    """Defines the operation where the mouse leaves the board rectangle."""
    if not self.getHoverBoardFlag():
      return False
    self.setNormalCursor()
    self.getBoardState().delHoverSquare()
    self.getBoardState().delHoverPiece()
    self.setHoverBoardFlag(False)
    self.update()
    return self.leaveEvent(event)

  def enterBoardRect(self, event: QMouseEvent) -> NoReturn:
    """Defines the operation where the mouse enters the board rectangle"""
    if self.getHoverBoardFlag():
      return
    self.setHoverBoardFlag(True)
    Sound.slide.play()
    if event is None:
      return self.update()
    enterEvent = Settings.convertToEnterEvent(self, event)
    return self.update() or self.enterEvent(enterEvent)

  def activateHoverSquare(self, event: QMouseEvent) -> NoReturn:
    """Applies hover to square given by the event if necessary."""
    point = event.position()
    boardRect = self.getBoardRect()
    square = Square.fromPointRect(point, boardRect)

    if square == self.getBoardState().hoverSquare:
      return self.update()
    self.getBoardState().hoverSquare = square
    return self.update()

  def activateHoverPiece(self, event: QMouseEvent) -> NoReturn:
    """Applies hover to the piece at the square"""
    boardState = self.getBoardState()
    if boardState.grabbedPiece:
      return
    point = event.position()
    boardRect = self.getBoardRect()
    square = Square.fromPointRect(point, boardRect)
    piece = boardState.getPiece(square)
    self.getBoardState().hoverPiece = piece

  def beginGrabbing(self, piece: ChessPiece, origin: Square) -> NoReturn:
    """Operation responsible for starting a grabbing operation."""
    if not isinstance(piece, ChessPiece):
      raise TypeError
    self.getBoardState().setGrabbedPiece(piece)
    self.setPieceCursor(piece)
    self.setOriginSquare(origin)
    self.getBoardState().setPiece(origin, ChessPiece.EMPTY)
    self.delHoverPiece()
    Sound.slide.play()
    self.update()

  def cancelGrabbing(self) -> NoReturn:
    """Defines the operation which cancels any ongoing grabbing operation"""
    originSquare, piece = self.getOriginSquare(), self.getGrabbedPiece()
    if not plenty(originSquare, piece):
      raise ProceduralError('Cancel grabbing')
    self.getBoardState().setPiece(originSquare, piece)
    self.setGrabbedPiece(ChessPiece.EMPTY)
    hoverSquare = self.getHoverSquare()
    hoverPiece = self.getBoardState().getPiece(hoverSquare)
    self.setHoverCursor()
    if isinstance(hoverPiece, ChessPiece):
      self.setHoverPiece(hoverPiece)
    Sound.whoosh.play()
    self.update()

  def completeGrabbing(self, *args) -> bool:
    """Completes the grabbing operation"""
    if not self.checkTarget():
      return self.cancelGrabbing()
    if args:
      warn('Unexpected positional arguments received!')
    piece = self.getGrabbedPiece()
    if not piece:
      return False
    self.delGrabbedPiece()
    self.getBoardState().setPiece(self.getHoverSquare(), piece)
    self.setHoverPiece(piece)
    self.setHoverCursor()
    self.update()
    Sound.move.play()
    return True
