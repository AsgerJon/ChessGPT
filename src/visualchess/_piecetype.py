"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum, IntEnum
from typing import TYPE_CHECKING, NoReturn

from icecream import ic
from worktoy.core import plenty
from worktoy.parsing import maybeType

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class Board:
  """Board representation"""

  @staticmethod
  def parseComplex(*args, **kwargs) -> complex:
    """Parses arguments to a complex number"""
    fileKwarg = kwargs.get('file', None)
    rankKwarg = kwargs.get('rank', None)
    complexArg = maybeType(complex, *args)
    if plenty(fileKwarg, rankKwarg):
      if isinstance(fileKwarg, int) and isinstance(rankKwarg, int):
        return fileKwarg + rankKwarg * 1j
    if isinstance(complexArg, complex):
      return complexArg

  def __init__(self) -> None:
    self._board = {}
    for x in range(8):
      for y in range(8):
        self._board |= {x + y * 1j: 0}

  def __getitem__(self, complexArg: complex) -> int:
    """Gets the piece at the given square"""
    if isinstance(complexArg, complex):
      return self._board.get(complexArg)

  def __setitem__(self, complexArg: complex, value: int) -> NoReturn:
    """Gets the piece at the given square"""
    if isinstance(complexArg, complex):
      return self._board.get(complexArg)

  def getFileRank(self, file: int, rank: int) -> int:
    """Wrapper allowing for integer keywords"""
    return self[file + rank * 1j]


class Color(IntEnum):
  """Color enum"""
  WHITE = -1
  NULL = 0
  BLACK = 1


class PieceType(IntEnum):
  """Types of chess pieces"""
  BLACK_KING = 6
  BLACK_QUEEN = 5
  BLACK_ROOK = 4
  BLACK_BISHOP = 3
  BLACK_KNIGHT = 2
  BLACK_PAWN = 1
  EMPTY = 0
  WHITE_PAWN = -1
  WHITE_KNIGHT = -2
  WHITE_BISHOP = -3
  WHITE_ROOK = -4
  WHITE_QUEEN = -5
  WHITE_KING = -6

  def relative(self, ) -> list[complex]:
    """The reach returns the points the piece could reach relative to
    some origin."""

    out = []
    if self is PieceType.EMPTY:
      return out

    if self is PieceType.BLACK_PAWN:
      return [-1 + 1j, 1j, 1 + 1j, 2j]
    if self is PieceType.WHITE_PAWN:
      return [-1 * arg for arg in [-1 + 1j, 1j, 1 + 1j, 2j]]

    if self is PieceType.WHITE_KNIGHT or PieceType.BLACK_KNIGHT:
      up = 1 + 2j
      down = 1 - 2j
      for _ in range(4):
        out.append(up)
        out.append(down)
        up *= 1j
        down *= 1j
      return out

    if self is PieceType.WHITE_BISHOP or PieceType.BLACK_BISHOP:
      for i in range(-7, 8):
        if i:
          lol = [1 + 1j, 1 - 1j, ]
          for item in lol:
            out.append(item * i)
      return [arg for arg in out if arg]

    if self is PieceType.WHITE_ROOK or PieceType.BLACK_ROOK:
      for i in range(-7, 8):
        if i:
          out.append(i)
          out.append(i * 1j)
      return [arg for arg in out if arg]

    if self is PieceType.WHITE_QUEEN or PieceType.BLACK_QUEEN:
      bishop = PieceType.BLACK_BISHOP.relative()
      rook = PieceType.BLACK_ROOK.relative()
      return [*bishop, *rook]

    if self is PieceType.BLACK_KING or PieceType.WHITE_KING:
      return [1 + 1j, 1, 1 - 1j, 0 + 1j, 0 - 1j, -1 - 1j, -1, -1 + 1j]

  def fromSquare(self, square: complex) -> list[complex]:
    """The reach returns the points the piece could reach from given
    origin."""
    out = []
    if self is PieceType.EMPTY:
      return []

    for arg in [square + p for p in self.relative()]:
      if max(abs(arg.real), abs(arg.imag)) < 8:
        if self is PieceType.BLACK_PAWN or self is PieceType.WHITE_PAWN:
          if int(arg.imag) in [1, 6]:
            out.append(arg)
          elif max(abs(arg.real), abs(arg.imag)) < 2:
            out.append(arg)
        else:
          out.append(arg)
    return [arg for arg in out if arg != square]

  def lineOfSight(self, boardState: Board) -> list[complex]:
    """Line of Sight restricts non-knights to not jump over pieces."""
