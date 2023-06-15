"""KingMove specifies an enum for one-step moves. These do not apply to pawn,
knight and king."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Never

from icecream import ic
from worktoy.stringtools import stringList, monoSpace
from worktoy.waitaminute import ReadOnlyError, UnexpectedStateError

from visualchess import PieceType, ChessColor

ic.configureOutput(includeContext=True)


class PieceMove(Enum):
  """KingMove enum"""
  UP1 = (0, 1)
  DOWN1 = (0, -1)
  LEFT1 = (-1, 0)
  RIGHT1 = (1, 0)
  UPRIGHT1 = (1, 1)
  UPLEFT1 = (-1, 1)
  DOWNLEFT1 = (-1, -1)
  DOWNRIGHT1 = (1, -1)
  UP2 = (0, 2)
  DOWN2 = (0, -2)
  LEFT2 = (-2, 0)
  RIGHT2 = (2, 0)
  UPRIGHT2 = (2, 2)
  UPLEFT2 = (-2, 2)
  DOWNLEFT2 = (-2, -2)
  DOWNRIGHT2 = (2, -2)
  UP3 = (0, 3)
  DOWN3 = (0, -3)
  LEFT3 = (-3, 0)
  RIGHT3 = (3, 0)
  UPRIGHT3 = (3, 3)
  UPLEFT3 = (-3, 3)
  DOWNLEFT3 = (-3, -3)
  DOWNRIGHT3 = (3, -3)
  UP4 = (0, 4)
  DOWN4 = (0, -4)
  LEFT4 = (-4, 0)
  RIGHT4 = (4, 0)
  UPRIGHT4 = (4, 4)
  UPLEFT4 = (-4, 4)
  DOWNLEFT4 = (-4, -4)
  DOWNRIGHT4 = (4, -4)
  UP5 = (0, 5)
  DOWN5 = (0, -5)
  LEFT5 = (-5, 0)
  RIGHT5 = (5, 0)
  UPRIGHT5 = (5, 5)
  UPLEFT5 = (-5, 5)
  DOWNLEFT5 = (-5, -5)
  DOWNRIGHT5 = (5, -5)
  UP6 = (0, 6)
  DOWN6 = (0, -6)
  LEFT6 = (-6, 0)
  RIGHT6 = (6, 0)
  UPRIGHT6 = (6, 6)
  UPLEFT6 = (-6, 6)
  DOWNLEFT6 = (-6, -6)
  DOWNRIGHT6 = (6, -6)
  UP7 = (0, 7)
  DOWN7 = (0, -7)
  LEFT7 = (-7, 0)
  RIGHT7 = (7, 0)
  UPRIGHT7 = (7, 7)
  UPLEFT7 = (-7, 7)
  DOWNLEFT7 = (-7, -7)
  DOWNRIGHT7 = (7, -7)
  Knight30 = (1, 2)
  Knight60 = (2, 1)
  Knight120 = (2, -1)
  Knight150 = (1, -2)
  Knight210 = (-1, -2)
  Knight240 = (-2, -1)
  Knight300 = (-2, 1)
  Knight330 = (-1, 2)

  @classmethod
  def getUpMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going UP"""
    return [cls.UP1, cls.UP2, cls.UP3, cls.UP4, cls.UP5, cls.UP6, cls.UP7, ]

  @classmethod
  def getRightMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going RIGHT"""
    return [cls.RIGHT1, cls.RIGHT2, cls.RIGHT3, cls.RIGHT4, cls.RIGHT5,
            cls.RIGHT6, cls.RIGHT7, ]

  @classmethod
  def getDownMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going DOWN"""
    return [cls.DOWN1, cls.DOWN2, cls.DOWN3, cls.DOWN4, cls.DOWN5, cls.DOWN6,
            cls.DOWN7, ]

  @classmethod
  def getLeftMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going LEFT"""
    return [cls.LEFT1, cls.LEFT2, cls.LEFT3, cls.LEFT4, cls.LEFT5, cls.LEFT6,
            cls.LEFT7, ]

  @classmethod
  def getUpRightMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going UPRIGHT"""
    return [cls.UPRIGHT1, cls.UPRIGHT2, cls.UPRIGHT3, cls.UPRIGHT4,
            cls.UPRIGHT5, cls.UPRIGHT6, cls.UPRIGHT7, ]

  @classmethod
  def getDownRightMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going DOWNRIGHT"""
    return [cls.DOWNRIGHT1, cls.DOWNRIGHT2, cls.DOWNRIGHT3, cls.DOWNRIGHT4,
            cls.DOWNRIGHT5, cls.DOWNRIGHT6, cls.DOWNRIGHT7, ]

  @classmethod
  def getDownLeftMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going DOWNLEFT"""
    return [cls.DOWNLEFT1, cls.DOWNLEFT2, cls.DOWNLEFT3, cls.DOWNLEFT4,
            cls.DOWNLEFT5, cls.DOWNLEFT6, cls.DOWNLEFT7, ]

  @classmethod
  def getUpLeftMoves(cls) -> list[PieceMove]:
    """Getter-function for all moves going UPLEFT"""
    return [cls.UPLEFT1, cls.UPLEFT2, cls.UPLEFT3, cls.UPLEFT4, cls.UPLEFT5,
            cls.UPLEFT6, cls.UPLEFT7, ]

  @classmethod
  def getKingMoves(cls) -> list[PieceMove]:
    """Getter-function for the list of king moves"""
    return [cls.UP1, cls.LEFT1, cls.UPRIGHT1, cls.UPLEFT1,
            cls.DOWNLEFT1, cls.DOWNRIGHT1, cls.DOWN1, cls.RIGHT1]

  @classmethod
  def getKnightMoves(cls) -> list[PieceMove]:
    """Getter-function for the knight moves"""
    return [cls.Knight30, cls.Knight60, cls.Knight120, cls.Knight150,
            cls.Knight210, cls.Knight240, cls.Knight300, cls.Knight330, ]

  @classmethod
  def getRookMoves(cls) -> list[PieceMove]:
    """Getter-function for the Rook moves"""
    return [*cls.getUpMoves(), *cls.getDownMoves(),
            *cls.getRightMoves(), *cls.getLeftMoves()]

  @classmethod
  def getBishopMoves(cls) -> list[PieceMove]:
    """Getter-function for the bishop moves"""
    return [*cls.getUpRightMoves(), *cls.getDownRightMoves(),
            *cls.getDownLeftMoves(), *cls.getUpLeftMoves()]

  @classmethod
  def getQueenMoves(cls) -> list[PieceMove]:
    """Getter-function for the queen moves"""
    return [*cls.getUpRightMoves(), *cls.getDownRightMoves(),
            *cls.getDownLeftMoves(), *cls.getUpLeftMoves(),
            *cls.getUpMoves(), *cls.getDownMoves(),
            *cls.getRightMoves(), *cls.getLeftMoves()]

  @classmethod
  def getWhitePawnMoves(cls) -> list[PieceMove]:
    """Getter-function for the white pawn moves.

    Please note that this does not include the special moves: two square
    move from initial square and promotion. The normal capture move also
    applies to the capture of en passant. Whether such is available
    depends on the piece position and the board state. This applies to the
    black pawns as well"""
    return [cls.UPLEFT1, cls.UP1, cls.UPRIGHT1]

  @classmethod
  def getBlackPawnMoves(cls) -> list[PieceMove]:
    """Getter-function for the black pawn moves."""
    return [cls.DOWNLEFT1, cls.DOWN1, cls.DOWNRIGHT1]

  @classmethod
  def getColorPawnMoves(cls, color: ChessColor) -> list[PieceMove]:
    """Getter-function for the pawn moves matching the given color"""
    out = None
    if color is ChessColor.WHITE:
      out = cls.getWhitePawnMoves()
    if color is ChessColor.BLACK:
      out = cls.getBlackPawnMoves()
    if out is None:
      msg = """Given color: %s is not a valid chess piece color!"""
      raise ValueError(msg % color)
    if isinstance(out, list):
      if all([isinstance(p, PieceMove) for p in out]):
        return out
      msg = """Found unexpected type in list of piece moves"""
      raise UnexpectedStateError(msg)
    msg = """Expected list of piece moves to be of type list, 
    but received: %s"""
    raise TypeError(monoSpace(msg) % type(out))

  @classmethod
  def getTypeMoves(cls, piece: PieceType) -> list[PieceMove]:
    """Getter-function for the moves """
    # if isinstance(piece, ChessPiece):
    #   return cls.getTypeMoves(piece.piece)
    return {
      PieceType.KNIGHT: cls.getKnightMoves(),
      PieceType.BISHOP: cls.getBishopMoves(),
      PieceType.ROOK  : cls.getRookMoves(),
      PieceType.QUEEN : [*cls.getRookMoves(), *cls.getBishopMoves()],
      PieceType.KING  : cls.getKingMoves(), }.get(piece)

  #
  # def __add__(self, other: Square) -> Optional[Square]:
  #   """Offsets the given square if possible"""
  #   x, y = other.x + self.x, other.y + self.y
  #   if -1 < x < 8 and -1 < y < 8:
  #     return Square.fromInts(x, y)
  #   return None
  #
  # def __sub__(self, other: Square) -> Optional[Square]:
  #   """Offsets the given square if possible"""
  #   x, y = other.x - self.x, other.y - self.y
  #   if -1 < x < 8 and -1 < y < 8:
  #     return Square.fromInts(x, y)
  #   return None
  #
  # def __radd__(self, other: Square) -> Optional[Square]:
  #   """Offsets the given square if possible"""
  #   return self + other
  #
  # def __rsub__(self, other: Square) -> Optional[Square]:
  #   """Offsets the given square if possible"""
  #   return self - other

  def _getX(self) -> int:
    """Getter-function for horizontal move"""
    return self.value[0]

  def _getY(self) -> int:
    """Getter-function for vertical move"""
    return self.value[1]

  def _noSet(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('move')

  @classmethod
  def fromValue(cls, file: int, rank: int) -> PieceMove:
    """Finds the move matching the given values as integers"""
    for instance in cls:
      if instance.x == file and instance.y == rank:
        return instance
    raise KeyError

  def __invert__(self) -> PieceMove:
    """Inverts the move"""
    x, y = -self.x, -self.y
    return self.fromValue(x, y)

  x = property(_getX, _noSet, _noSet)
  y = property(_getX, _noSet, _noSet)

  def __str__(self) -> str:
    """String Representation"""
    board = [stringList('X, X, X, X, X, X, X') for _ in range(7)]
    board[3][3] = '0'
    board[3 + self.y][3 + self.x] = '1'
    return '\n'.join(['-'.join(rank) for rank in board])
