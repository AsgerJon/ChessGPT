"""KingMove subclasses ChessMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from icecream import ic

from visualchess import ChessMove, StateChange, ChessPiece

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class KingMove(ChessMove):
  """KingMove subclasses RegularMove
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return True if self.sourcePiece.isKing else False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """All moves that are no longer than 1 square away from source are
    possible."""
    dx, dy = self.sourceX - self.targetX, self.sourceY - self.targetY
    return False if dx ** 2 > 1 or dy ** 2 > 1 else True

  def updateBoardState(self) -> list[StateChange]:
    """Places the king at the target square"""
    out = [self.state.setPiece(self.targetSquare, self.sourcePiece),
           self.state.setPiece(self.sourceSquare, ChessPiece.EMPTY)]
    return out
