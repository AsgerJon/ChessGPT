"""KingMove subclasses RegularMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic
from worktoy.core import maybe, plenty

from visualchess import RegularMove, Move, ChessPiece

ic.configureOutput(includeContext=True)


class KingMove(RegularMove):
  """KingMove subclasses RegularMove
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    RegularMove.__init__(self, *args, **kwargs)

  def validateMove(self, *args, **kwargs) -> bool:
    """Implementation of move validation. Please note the use of the
    equality operator instead of the 'is' keyword. This is because the
    NULL color is equal to nothing not even itself. Thus the condition at
    the top will trigger only when both colors are 'black' or 'white'."""
    if not self.baseValidation():
      return False

  def applyMove(self, *args, **kwargs) -> NoReturn:
    RegularMove.applyMove(self, *args, **kwargs)

  def __str__(self) -> str:
    """String Representation"""
    if self.validateMove():
      msg = """Moves %s king from %s to %s."""
      color = '%s' % (self.state.grabbedPiece.color)
      source = '%s' % (self.state.grabbedSquare)
      target = '%s' % (self.state.hoverSquare)
      return msg % (color, source, target)

  def __repr__(self, ) -> str:
    """Code Representation"""
    return '%s' % self.state.move
