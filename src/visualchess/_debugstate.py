"""DebugState is a subuclass of BoardState allowing for debugging"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic
from worktoy.stringtools import stringList

from visualchess import BoardState, Square, PieceType

ic.configureOutput(includeContext=True)


class DebugState(BoardState):
  """DebugState is a subclass of BoardState allowing for debugging"""

  def __init__(self, *args, **kwargs) -> None:
    BoardState.__init__(self, *args, **kwargs)

  def debug(self) -> NoReturn:
    """Debugger"""

  def getMoves(self, square: Square) -> list[Square]:
    """Returns the list of moves available to the piece currently
    occupying the given square."""
    if self.getPiece(square) in PieceType.KING:
      return self.getKingSquares(square)
