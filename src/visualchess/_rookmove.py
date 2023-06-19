"""RookMove subclasses ChessMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from visualchess import ChessMove, Square

ic.configureOutput(includeContext=True)


class RookMove(ChessMove):
  """RookMove subclasses ChessMove
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return True if self.sourcePiece.isRook else False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """Rooks can move between squares that share either their file or
    their rank."""
    x0, y0, x1, y1 = self.sourceX, self.sourceY, self.targetX, self.targetY
    return False if (x1 - x0) * (y1 - y0) else True
