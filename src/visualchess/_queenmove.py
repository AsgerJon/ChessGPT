"""QueenMove subclasses ChessMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, ChessPiece, StateChange

ic.configureOutput(includeContext=True)


class QueenMove(ChessMove):
  """QueenMove subclasses ChessMove
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return True if self.sourcePiece.isQueen else False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """All moves that are no longer than 1 square away from source are
    possible."""
    dx = abs(self.sourceX - self.targetX)
    dy = abs(self.sourceY - self.targetY)
    return False if (dx - dy) * dx * dy else True

  def updateBoardState(self) -> list[StateChange]:
    """Places the king at the target square"""
    ic()
    out = [self.state.setPiece(self.targetSquare, self.sourcePiece),
           self.state.setPiece(self.sourceSquare, ChessPiece.EMPTY)]
    return out
