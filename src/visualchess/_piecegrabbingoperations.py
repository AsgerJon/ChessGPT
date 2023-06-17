"""The '_PieceGrabbingOperations' class defines the operations used by the
PieceGrabbing widget."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QEvent
from PySide6.QtGui import QMouseEvent
from icecream import ic

from visualchess import _PieceGrabbingProperties, ChessPiece
from visualchess import Square

ic.configureOutput(includeContext=True)


class _PieceGrabbingOperations(_PieceGrabbingProperties):
  """The '_PieceGrabbingOperations' class defines the operations used by the
  PieceGrabbing widget.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)
    self._cancelGrabbingOperation = None

  def activateHoverSquare(self, event: QMouseEvent) -> NoReturn:
    """Applies hover to square given by the event if necessary."""
    point = event.position()
    boardRect = self.getBoardRect()
    square = Square.fromPointRect(point, boardRect)
    self.getBoardState().hover(square)
    if self.getBoardState().grabbedPiece:
      return self.update()
    piece = self.getBoardState().getPiece(square)
    if piece:
      if piece.color == self.getBoardState().colorTurn:
        self.setHoverCursor()
      else:
        self.setForbiddenCursor()
    else:
      self.setNormalCursor()
    self.update()

  def beginGrabbing(self, piece: ChessPiece, ) -> NoReturn:
    """Operation responsible for starting a grabbing operation."""
    if self.getBoardState().grabPiece():
      self.setPieceCursor(piece)
    self.update()

  def completeGrabbing(self) -> NoReturn:
    """Completes the grabbing operation"""
    if self.getBoardState().grabbedPiece:
      self.getBoardState().applyMove()
      self.setHoverCursor()
    self.update()
