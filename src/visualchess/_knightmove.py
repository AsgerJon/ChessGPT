"""KnightMove subclasses RegularMove and implements knight moves"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, Square

ic.configureOutput(includeContext=True)


class KnightMove(ChessMove):
  """KnightMove subclasses RegularMove and implements knight moves.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return True if self.sourcePiece.isKnight else False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """The greater step is 2 and the lesser step is 1. """
    dx = abs(self.sourceX - self.targetX)
    dy = abs(self.sourceY - self.targetY)
    return True if min(dx, dy) == 1 and max(dx, dy) == 2 else False

  def updateBoardState(self, *args, **kwargs) -> NoReturn:
    """Places the knight at the target square"""
    self.state.setPiece(self.targetSquare, self.sourcePiece)
