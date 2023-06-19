"""LongCastle subclasses ChessMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from visualchess import ChessMove, File, Rank

ic.configureOutput(includeContext=True)


class LongCastle(ChessMove):
  """LongCastle subclasses ChessMove
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
    if self.sourceFile is not File.E:
      return False
    if not (self.sourceRank is Rank.rank1 or self.sourceRank is Rank.rank8):
      return False
    if self.targetFile is not File.C:
      return False
    if not (self.targetRank is Rank.rank1 or self.targetRank is Rank.rank8):
      return False
