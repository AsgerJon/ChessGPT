"""Enums are necessary to have consistency across the modules"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.stringtools import stringList
from worktoy.typetools import TypeBag

if TYPE_CHECKING:
  from visualchess import Square

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)

_pieces = stringList('King, Queen, Rook, Bishop, Knight, Pawn')
_colors = stringList('white, black')


class Diagonal(IntEnum):
  """Like File and Rank, the Diagonals represent diagonal lines. They are
  identified by the file of the diagonal at row 1 as well as a sign.
  Positive means that as File increases from A through H, ranks increase,
  whereas negative indicates decreasing ranks. Like File and Rank,
  the integer value of a diagonal is hidden. Instead, the diagonals are
  named [File][LeftOrRight] as seen from both players. For example,
  AL means the diagonal starting at A1 going through H2, G3..."""

  AL = -1
  BL = -2
  CL = -3
  DL = -4
  EL = -5
  FL = -6
  GL = -7
  HL = -8
  _PLACEHOLDER = 0
  AR = 1
  BR = 2
  CR = 3
  DR = 4
  ER = 5
  FR = 6
  GR = 7
  HR = 8

  @classmethod
  def leftFile(cls, file: File) -> Diagonal:
    """Creates a Diagonal instance from the given file sloping left."""

  @classmethod
  def rightFile(cls, file: File) -> Diagonal:
    """Creates a Diagonal instance from the given file sloping right."""

  @classmethod
  def fromStr(cls, name: str) -> Diagonal:
    """Finds an instance from the given string"""
    if len(name) != 2:
      msg = """Diagonal names must be two characters, but received: %s of 
      length %d!"""
      raise ValueError(msg % (name, len(name)))
    for item in cls:
      if item.name == name:
        return item
    msg = """Unable to recognize given name as a diagonal: %s!"""
    raise ValueError(msg % name)

  @classmethod
  def fromValue(cls, value: int) -> Diagonal:
    """Finds the matching value"""
    for diagonal in Diagonal:
      if diagonal.value == value:
        return diagonal
    raise TypeError

  def getSquares(self) -> list[Square]:
    """Returns a list of squares contained in this diagonal"""
    squares = []
    file = File.fromStr(self.name[0])
    for (i, rank) in enumerate(Rank):
      squares.append(Square.fromFileRank(file, rank))
    return []
