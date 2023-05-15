"""LegalMove represents a legal move"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from visualchess import Piece, Square


class LegalMove:
  """LegalMove represents a legal move
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    self._sourcePiece: Optional[Piece] = None
    self._targetPiece: Optional[Piece] = None
    self._sourceSquare: Optional[Square] = None
    self._targetSquare: Optional[Square] = None
