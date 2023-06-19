"""BishopMove subclasses ChessMove """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, Square

ic.configureOutput(includeContext=True)


class BishopMove(ChessMove):
  """BishopMove subclasses ChessMove.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return True if self.sourcePiece.isBishop else False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """All moves that are no longer than 1 square away from source are
    possible."""
    dx = abs(self.sourceX - self.targetX)
    dy = abs(self.sourceY - self.targetY)
    return True if dx == dy else False

  def updateBoardState(self, *args, **kwargs) -> NoReturn:
    """Places the bishop at the target square"""
    self.state.setPiece(self.targetSquare, self.sourcePiece)
