"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError, ProceduralError

from visualchess import ChessPiece, Square, Move
from visualchess.chesspieces import initialPosition

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)


class BoardState:
  """BoardState represents a chess board with each squared occupied by a
  member, possibly the empty one, of the Piece Enum."""

  @classmethod
  def InitialPosition(cls) -> BoardState:
    """Creates an instance with piece at the starting position"""
    instance = cls()
    for line in initialPosition:
      square = Square.fromStr(line[0])
      piece = ChessPiece.fromColorPiece(line[1], line[2])
      instance[square] = piece
    return instance

  def __init__(self, *args, **kwargs) -> None:
    self._contents = {s: ChessPiece.EMPTY for s in Square}

  def __getitem__(self, square: Square) -> ChessPiece:
    """Returns the piece at given square"""
    return self._contents.get(square)

  def __setitem__(self, square: Square, piece: ChessPiece) -> NoReturn:
    """Places given piece and given square"""
    self._contents |= {square: piece}

  def __delitem__(self, square: Square) -> NoReturn:
    """Deletes the item at given square. Deleting means placing the EMPTY
    piece."""
    self._contents |= {square: ChessPiece.EMPTY}

  def keys(self) -> list[Square]:
    """Implementation of keys method"""
    return [key for key in self._contents.keys()]

  def values(self) -> list[ChessPiece]:
    """Implementation of values"""
    return [piece for piece in self._contents.values()]

  def items(self) -> list[tuple[Square, ChessPiece]]:
    """Implementation of items method"""
    return [(k, v) for (k, v) in self._contents.items()]

  def getPiece(self, square: Square) -> ChessPiece:
    """Getter-function for the piece on the given square"""
    piece = self._contents.get(square, None)
    if piece is not None:
      if isinstance(piece, ChessPiece):
        return piece
      raise TypeError
    os.abort()
    raise UnexpectedStateError

  def setPiece(self, square: Square, piece: ChessPiece) -> NoReturn:
    """Setter-function for the piece on the given square"""
    if piece is not None:
      if isinstance(piece, ChessPiece):
        self._contents[square] = piece
      else:
        raise TypeError
    else:
      raise UnexpectedStateError

  def delPiece(self, square: Square) -> ChessPiece:
    """Deleter-function for the given square. This removes the piece from
    it. Invoking the deleter returns the chess piece"""
    piece = self.getPiece(square)
    self.setPiece(square, ChessPiece.EMPTY)
    return piece

  def getMoveSquares(self, square: Square) -> list[Square]:
    """Getter-function for the squares to which the piece on the given
    square can move."""
    if not self.getPiece(square):
      return []

  def pieceGuard(self, piece: ChessPiece | str, square: Square) -> bool:
    """This method checks if the given piece is on the given square.
    Please note that this method is color agnostic meaning that it returns
    true regardless of what color the piece is."""
    placedPiece = self.getPiece(square)
    if not placedPiece:
      return False
    return True if piece in [placedPiece, ~placedPiece] else False

  def getKingSquares(self, square: Square, **kwargs) -> list[Square]:
    """Getter-function for the squares reachable by a king on the given
    square. This method raises an exception a king is not on the given
    square. Suppress this error by setting keyword argument 'strict' to
    False (default is True).

    Please note that this method will return moves that would put the king
    in check! Such moves a removed by a separate method which removes all
    moves which would put the king in check. This method does remove moves
    that would bring the piece out of bounds."""
    piece, out = self.getPiece(square), []
    if not self.pieceGuard(piece, square):
      msg = """Expected """
      raise ProceduralError(msg % (square, self.getPiece(square)))
    for move in Move.getKingMoves():
      out.append(square + move)
    return [move for move in out if move is not None]

  def getKnightSquares(self, square: Square, **kwargs) -> list[Square]:
    """Getter-function for the knight moves. See docstring for king moves."""
    knights = [ChessPiece.WHITE_KNIGHT, ChessPiece.BLACK_KNIGHT]
    piece, out = self.getPiece(square), []
    if piece not in knights and kwargs.get('strict', True):
      msg = """Expected a knight on square %s, but found instead: %s"""
      raise ProceduralError(msg % (square, self.getPiece(square)))
    for move in Move.getKnightMoves():
      out.append(square + move)
    return [move for move in out if move is not None]

  def getRookSquares(self, square: Square, **kwargs) -> list[Square]:
    """Getter-function for the squares reachable by a rook from the given
    square. Set keyword argument 'strict' to False to allow even if a rook
    is not on the square. By default this would raise an error. """
    