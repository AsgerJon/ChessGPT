"""EmptyMove is a subclass of ChessMove defining a move that should not be
completed."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, ChessAudio

ic.configureOutput(includeContext=True)


class EmptyMove(ChessMove):
  """EmptyMove is a subclass of ChessMove defining a move that should not be
  completed.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """All moves that are no longer than 1 square away from source are
    possible."""
    return False

  def updateBoardState(self) -> NoReturn:
    """Places the king at the target square"""
    ChessAudio.soundCancelMove.play()
