"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import cmath
from enum import Enum, IntEnum
import os
from typing import TYPE_CHECKING, NoReturn, Never

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPixmap, QColor, QCursor
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError
from icecream import ic

from visualchess import Square

if TYPE_CHECKING:
  pass

pi = 3.1415_9265_3589_793

ic.configureOutput(includeContext=True)


class OctRose(Enum):
  """OctRose represents the eight directions. """
  NULL = 0
  RIGHT = 1 + 0j
  UPRIGHT = 1 + 1j
  UP = 0 + 1j
  UPLEFT = -1 + 1j
  LEFT = -1 + 0j
  DOWNLEFT = -1 - 1j
  DOWN = 0 - 1j
  DOWNRIGHT = 1 - 1j

  def phase(self) -> float:
    """Getter-function for the phase of the instance"""
    return cmath.phase(self.value)

  def __bool__(self, ) -> bool:
    """NULL is False others are True"""
    return False if self is OctRose.NULL else True

  def __eq__(self, other: OctRose) -> bool:
    """Items are only equal to themselves except for NULL which is not
    even to itself."""
    if self and other and self is other:
      return True
    return False

  @classmethod
  def fromSquares(cls, source: complex, target: complex) -> OctRose:
    """Returns the member having the direction as the direction spanning
    from source to target"""
    argPhase = cmath.phase(target - source)
    for instance in cls:
      if instance:
        if (instance.phase() - argPhase) ** 2 < 1e-09:
          return instance
    return cls.NULL


class Color(IntEnum):
  """Color enum"""
  WHITE = -1
  NULL = 0
  BLACK = 1


class GameState:
  """GameState representation"""

  @staticmethod
  def getVector(source: complex, target: complex) -> tuple[complex, ...]:
    """Getter-function for vector pointing from source to target"""
    dx, dy = target.real - source.real, target.imag - source.imag
    v = None
    if (not dx) and dy:
      v = 1j if dy > 0 else -1j
    elif (not dy) and dx:
      v = 1 if dx > 0 else -1
    elif abs(dx) == abs(dy):
      v = dx / abs(dx) + dy / abs(dy) * 1j
    return (v, dx, dy)

  def lineOfSight(self, source: complex, target: complex) -> bool:
    """Checks if a straight path of empty squares are present between two
    squares. If they are adjacent having no squares in between,
    it is treated as a True value. If the two squares are in fact the same
    square, it returns False. A True return value from this method implies
    the availability of a move from source to target, which requires
    them to be distinct. """
    v, dx, dy = self.getVector(source, target)
    if v is None:
      return False
    dx, dy = int(float(dx.real)), int(float(dy.real)),
    d = max(dx, dy)
    if d == 1:
      return True
    for i in range(1, d):
      if isinstance((source + v * i), complex):
        if self[(source + v * i)]:
          return False
    return True

  def __init__(self) -> None:
    self._board = {}
    for x in range(8):
      for y in range(8):
        self._board |= {x + y * 1j: 0}
    self.setInitialPosition()

  def __getitem__(self, key: complex | Square) -> int:
    """Gets the piece at the given square"""
    if isinstance(key, complex):
      return self._board.get(key)

  def __setitem__(self, key: complex, piece: PieceType) -> NoReturn:
    """Gets the piece at the given square"""
    if isinstance(key, complex):
      return self._board.get(key)

  def items(self, ) -> list[tuple[Square, PieceType]]:
    """Implementation of items"""
    out = []
    for square in Square:
      out.append((square, PieceType.fromValue(self[square.getComplex()])))
    if isinstance(out, list):
      return out

  def clearBoard(self, ) -> NoReturn:
    """Clears the board by setting all squares to 0"""
    keys = [key for (_, key) in self._board.items()]
    self._board = {key: 0 for key in keys}

  def setInitialPosition(self) -> NoReturn:
    """Sets the initial board position"""
    self[0 + 0 * 1j] = PieceType.BLACK_ROOK
    self[7 + 0 * 1j] = PieceType.BLACK_ROOK
    self[1 + 0 * 1j] = PieceType.BLACK_KNIGHT
    self[6 + 0 * 1j] = PieceType.BLACK_KNIGHT
    self[2 + 0 * 1j] = PieceType.BLACK_BISHOP
    self[5 + 0 * 1j] = PieceType.BLACK_BISHOP
    self[3 + 0 * 1j] = PieceType.BLACK_QUEEN
    self[4 + 0 * 1j] = PieceType.BLACK_KING

    self[0 + 1 * 1j] = PieceType.BLACK_PAWN
    self[7 + 1 * 1j] = PieceType.BLACK_PAWN
    self[1 + 1 * 1j] = PieceType.BLACK_PAWN
    self[6 + 1 * 1j] = PieceType.BLACK_PAWN
    self[2 + 1 * 1j] = PieceType.BLACK_PAWN
    self[5 + 1 * 1j] = PieceType.BLACK_PAWN
    self[3 + 1 * 1j] = PieceType.BLACK_PAWN
    self[4 + 1 * 1j] = PieceType.BLACK_PAWN

    self[0 + 7 * 1j] = PieceType.WHITE_ROOK
    self[7 + 7 * 1j] = PieceType.WHITE_ROOK
    self[1 + 7 * 1j] = PieceType.WHITE_KNIGHT
    self[6 + 7 * 1j] = PieceType.WHITE_KNIGHT
    self[2 + 7 * 1j] = PieceType.WHITE_BISHOP
    self[5 + 7 * 1j] = PieceType.WHITE_BISHOP
    self[3 + 7 * 1j] = PieceType.WHITE_QUEEN
    self[4 + 7 * 1j] = PieceType.WHITE_KING

    self[0 + 6 * 1j] = PieceType.WHITE_PAWN
    self[7 + 6 * 1j] = PieceType.WHITE_PAWN
    self[1 + 6 * 1j] = PieceType.WHITE_PAWN
    self[6 + 6 * 1j] = PieceType.WHITE_PAWN
    self[2 + 6 * 1j] = PieceType.WHITE_PAWN
    self[5 + 6 * 1j] = PieceType.WHITE_PAWN
    self[3 + 6 * 1j] = PieceType.WHITE_PAWN
    self[4 + 6 * 1j] = PieceType.WHITE_PAWN

  def fromSquare(self, square: complex | Square) -> list[complex]:
    """The reach returns the points the piece could reach from given
    origin."""
    if isinstance(square, Square):
      return self.fromSquare(square.getComplex())
    color, piece, out = None, self[square], []
    if isinstance(piece, PieceType):
      out, file, rank, color = [], square.real, square.imag, piece.color
    if piece is PieceType.EMPTY:
      return []
    if piece is PieceType.BLACK_PAWN or PieceType.WHITE_PAWN:
      rankMove = 1j if PieceType.BLACK_PAWN else -1j
      out = [square + rankMove, ]
      for p in [square - 1 + rankMove, square + 1 + rankMove]:
        if isinstance(p, complex):
          if -1 < p.real < 8 and -1 < p.imag < 8:
            if self[p] < 0 and color == Color.BLACK:
              out.append(p)
            if self[p] > 0 and color == Color.WHITE:
              out.append(p)
    if self in PieceType.oneHot():
      for step in piece.relative():
        target = square + step
        if -1 < target.real < 8 and -1 < target.imag < 8:
          if self[target] <= 0 and color == Color.BLACK:
            out.append(target)
          if self[target] >= 0 and color == Color.WHITE:
            out.append(target)
    if self in PieceType.rangeHot():
      for step in piece.relative():
        target = square + step
        if -1 < target.real < 8 and -1 < target.imag < 8:
          if self.lineOfSight(square, target):
            if self[target] <= 0 and color == Color.BLACK:
              out.append(target)
            if self[target] >= 0 and color == Color.WHITE:
              out.append(target)
    return out


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

  @classmethod
  def fromValue(cls, value: int) -> PieceType:
    """Returns the instance having given value"""
    for instance in cls:
      if instance.value == value:
        return instance
    return cls.EMPTY

  @classmethod
  def oneHot(cls) -> list[PieceType]:
    """Getter-function for the instance not requiring examination of the
    line of sight. This means kings and knights"""
    return [
      PieceType.BLACK_KING,
      PieceType.WHITE_KING,
      PieceType.BLACK_KNIGHT,
      PieceType.WHITE_KNIGHT,
    ]

  @classmethod
  def rangeHot(cls) -> list[PieceType]:
    """Getter-function for the instances requiring examination of the line
    of sight."""
    return [
      PieceType.WHITE_QUEEN,
      PieceType.WHITE_ROOK,
      PieceType.WHITE_BISHOP,
      PieceType.BLACK_QUEEN,
      PieceType.BLACK_ROOK,
      PieceType.BLACK_BISHOP,
    ]

  def getPixmap(self) -> QPixmap:
    """Generates QPixmap representation of the piece"""
    if not self.value:
      pix = QPixmap(64, 64)
      pix.fill(QColor(0, 0, 0, 0, ))
      return pix
    root = os.getenv('CHESSGPT')
    there = stringList('src, visualchess, chesspieces, images')
    os.path.join(root, *there)
    fileName = '%s.png' % self.name.lower()
    filePath = os.path.join(root, *there, fileName)
    return QPixmap(filePath)

  def getCursor(self, point: QPointF = None) -> QCursor:
    """Generates a QCursor instance at the given point as hot. Please
    note, that passing a point to this function will create a QCursor
    whose hot point is that point. The point defaults to origin which is
    likely safe for most situations."""
    pix = self.getPixmap()
    x, y = -1, -1
    if isinstance(point, QPointF):
      x, y = point.x(), point.y()
    return QCursor(pix, hotX=x, hotY=y)

  def _noSet(self, *_) -> Never:
    """Illegal accessor function"""
    raise ReadOnlyError('color')

  def _getColor(self) -> Color:
    """Getter-function for color"""
    return Color.BLACK if self.value > 0 else Color.WHITE

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

  color = property(_getColor, _noSet, _noSet)
