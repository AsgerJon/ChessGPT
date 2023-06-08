"""The '_PieceGrabbingOperations' class defines the operations used by the
PieceGrabbing widget."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic
from worktoy.core import plenty
from worktoy.waitaminute import ProceduralError

from visualchess import _PieceGrabbingProperties, ChessPiece

ic.configureOutput(includeContext=True)


class _PieceGrabbingOperations(_PieceGrabbingProperties):
  """The '_PieceGrabbingOperations' class defines the operations used by the
  PieceGrabbing widget.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)
    self._cancelGrabbingOperation = None

  def cancelGrabbing(self) -> NoReturn:
    """Defines the operation which cancels any ongoing grabbing operation"""
    originSquare, piece = self.getOriginSquare(), self.getGrabbedPiece()
    if not plenty(originSquare, piece):
      raise ProceduralError('Cancel grabbing')
    self.getBoardState().setPiece(originSquare, piece)
    self.setGrabbedPiece(ChessPiece.EMPTY)
    