"""EnPassant subclasses ChessMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, ChessPiece, Square, StateChange

ic.configureOutput(includeContext=True)


class EnPassantMove(ChessMove):
  """EnPassant subclasses ChessMove
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return True if self.sourcePiece.isPawn else False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """Checks if move is possible"""
    dx, dy = self.sourceX - self.targetX, self.sourceY - self.targetY
    if abs(dx) == 1 and abs(dy) == 1:
      return True

  def baseValidation(self, *args, **kwargs) -> bool:
    """Reimplementation of base validation. The special en passant
    procedure requires the target square to be empty instead of occupied
    by the opposite color."""
    if not self.state.enPassantFile == self.targetFile:
      return False
    if not self.sourceRank == self.sourceColor.getEnPassantRank():
      return False
    if self.state.getPiece(self.targetSquare):
      return False

  def updateBoardState(self) -> list[StateChange]:
    """Places the king at the target square"""
    enPassantSquare = Square.fromFileRank(self.targetFile, self.sourceRank)
    out = [
      self.state.setPiece(self.sourceSquare, ChessPiece.EMPTY),
      self.state.setPiece(self.targetSquare, self.sourcePiece),
      self.state.setPiece(enPassantSquare, ChessPiece.EMPTY)]
    return out
