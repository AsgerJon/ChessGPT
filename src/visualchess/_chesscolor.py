"""ChessColor enum"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum

from icecream import ic

ic.configureOutput(includeContext=True)


class ChessColor(Enum):
  """ChessColor enum"""
  WHITE = -1
  NULL = 0
  BLACK = 1

  def __str__(self) -> str:
    """String Representation"""
    if self is ChessColor.NULL:
      return 'Colorless'

    if self is ChessColor.WHITE:
      return 'White'

    if self is ChessColor.BLACK:
      return 'Black'

  def __repr__(self) -> str:
    """String Representation"""
    if self is ChessColor.NULL:
      return 'ChessColor.NULL'

    if self is ChessColor.WHITE:
      return 'ChessColor.WHITE'

    if self is ChessColor.BLACK:
      return 'ChessColor.BLACK'

  def __bool__(self) -> bool:
    """NULL is False, black and white are true"""
    if self is ChessColor.NULL:
      return False

    if self is ChessColor.WHITE or self is ChessColor.BLACK:
      return True

  def __eq__(self, other: ChessColor) -> bool:
    """Equality operator. NULL is not equal to itself"""
    if self is ChessColor.NULL or other is ChessColor.NULL:
      return False

    if self is ChessColor.WHITE and other is ChessColor.WHITE:
      return True

    if self is ChessColor.BLACK and other is ChessColor.BLACK:
      return True

  def __invert__(self) -> ChessColor:
    """Inverts. Black to white, white to black, null to null"""
    if self is ChessColor.NULL:
      return ChessColor.NULL
    
    if self is ChessColor.WHITE:
      return ChessColor.BLACK

    if self is ChessColor.BLACK:
      return ChessColor.WHITE
