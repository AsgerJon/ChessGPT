"""KnightMove subclasses RegularMove and implements knight moves"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from visualchess import RegularMove

ic.configureOutput(includeContext=True)


class KnightMove(RegularMove):
  """KnightMove subclasses RegularMove and implements knight moves.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    RegularMove.__init__(self, *args, **kwargs)

  def validateMove(self, *args, **kwargs) -> bool:
    """Implementation of move validation"""
