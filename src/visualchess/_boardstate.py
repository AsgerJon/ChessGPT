"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.stringtools import stringList, monoSpace
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, PieceMove, File, ChessColor, \
  PieceType
from visualchess.chesspieces import initialPosition

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)
PositionList = list[list[str]]

debugPosition = [
  stringList('E8, black, king'),
  stringList('E1, white, king'),
]


class BoardState:
  """BoardState represents a chess board with each squared occupied by a
  member, possibly the empty one, of the Piece Enum."""

  @classmethod
  def readList(cls, positionList: PositionList) -> BoardState:
    """Creates an instance with pieces as defined in the given list"""
    instance = cls()
    instance.updatePositionFromList(positionList)
    return instance

  @classmethod
  def InitialPosition(cls) -> BoardState:
    """Creates an instance with the starting position"""
    return cls.readList(initialPosition)

  @classmethod
  def DebugPosition(cls) -> BoardState:
    """Creates an instance with the debug position"""
    return cls.readList(debugPosition)

  def __init__(self, *args, **kwargs) -> None:
    self._contents = {s: ChessPiece.EMPTY for s in Square}
    self._activeColor = ChessColor.WHITE
    self._whiteEnPassant = {f: False for f in File}
    self._blackEnPassant = {f: False for f in File}
    self._castleFlag = {s: True for s in Square.getCorners()}

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

  def pieceGuard(self, piece: PieceType, square: Square) -> bool:
    """This method checks if the given piece is on the given square.
    Please note that this method is color agnostic meaning that it returns
    true regardless of what color the piece is."""
    placedPiece = self.getPiece(square)
    if not placedPiece:
      return False
    return True if piece in [placedPiece, ~placedPiece] else False

  def pieceGuardStrict(self, piece: PieceType, square: Square) -> bool:
    """This method raises an error if the piece guard fails"""
    if self.pieceGuard(piece, square):
      return True
    actualPiece = self.getPiece(square)
    msg = """Expected piece %s on square %s, but found %s!"""
    raise UnexpectedStateError(msg % (piece, square, actualPiece))

  def getKingSquares(self, square: Square, ) -> list[Square]:
    """Getter-function for the squares reachable by a king on the given
    square. This method raises an exception a king is not on the given
    square.

    Please note that this method will return moves that would put the king
    in check! Such moves a removed by a separate method which removes all
    moves which would put the king in check. This method does remove moves
    that would bring the piece out of bounds."""
    piece, out = self.getPiece(square), []
    self.pieceGuardStrict(PieceType.KING, square)
    for move in PieceMove.getKingMoves():
      out.append(square + move)
    return [move for move in out if move is not None]

  def getKnightSquares(self, square: Square, ) -> list[Square]:
    """Getter-function for the knight moves. See docstring for king moves."""
    piece, out = self.getPiece(square), []
    self.pieceGuardStrict(PieceType.KNIGHT, square)
    for move in PieceMove.getKnightMoves():
      out.append(square + move)
    return [move for move in out if move is not None]

  def getRookSquares(self, square: Square, ) -> list[Square]:
    """Getter-function for the squares reachable by a rook from the given
    square. """
    self.pieceGuardStrict(PieceType.ROOK, square)
    piece, out = self.getPiece(square), []
    for move in PieceMove.getRookMoves():
      movingSquare = square + move
      while not self.getPiece(movingSquare):
        out.append(movingSquare)
        movingSquare += move
      out.append(movingSquare)
    return out

  def getBishopSquares(self, square: Square) -> list[Square]:
    """Getter-function for the squares reachable by rook from the g iven
    square."""
    self.pieceGuardStrict(PieceType.BISHOP, square)
    piece, out = self.getPiece(square), []
    for move in PieceMove.getBishopMoves():
      movingSquare = square + move
      while not self.getPiece(movingSquare):
        out.append(movingSquare)
        movingSquare += move
      out.append(movingSquare)
    return out

  def getQueenSquares(self, square: Square) -> list[Square]:
    """Getter-function for the squares reachable by rook from the given
    square."""
    self.pieceGuardStrict(PieceType.QUEEN, square)
    rookMoves = self.getRookSquares(square)
    bishopMoves = self.getBishopSquares(square)
    return [*rookMoves, *bishopMoves]

  def getPawnSquares(self, square: Square) -> list[Square]:
    """Getter-function for the squares reachable by a pawn from the given
    square."""
    self.pieceGuardStrict(PieceType.QUEEN, square)
    if not self.getPiece(square):
      return []

  def getMoves(self, square: Square) -> list[Square]:
    """Getter-function for the moves available from the given square"""
    piece = self.getPiece(square)
    if not piece:
      return []
    if piece in ChessPiece.getKings():
      return self.getKingSquares(square)
    if piece in ChessPiece.getKnights():
      return self.getKnightSquares(square)
    if piece in ChessPiece.getBishops():
      return self.getBishopSquares(square)
    if piece in ChessPiece.getQueens():
      return self.getQueenSquares(square)
    if piece in ChessPiece.getRooks():
      return self.getRookSquares(square)
    if piece in ChessPiece.getPawns():
      return self.getPawnSquares(square)
    raise UnexpectedStateError

  def _getBlackEnPassant(self) -> dict[File, bool]:
    """Getter-function for dictionary containing en passant status on
    black side, that is for rank 6 which has enum integer 2"""
    return self._blackEnPassant

  def _getWhiteEnPassant(self) -> dict[File, bool]:
    """Getter-function for dictionary containing en passant status on
    white side, that is for rank 3 which has enum integer 5"""
    return self._whiteEnPassant

  def getEnPassant(self, square: Square) -> bool:
    """Getter function for whether the given square is en passant. Suppose
    the C pawn of WHITE is able to en passant to the left. Then the pawn
    on C5 has the move."""
    if (square.y - 3) * (square.y - 4):
      return False
    if square.y == 3:
      return self._getBlackEnPassant()[square.file]
    return self._getWhiteEnPassant()[square.file]

  def getCastlingFlag(self, corner: Square) -> bool:
    """Getter-function for the castling flag on the given square. Please
    note that this flag indicates if a particular corner is still
    available for castling. It does not check if castling is actually
    possible. If the white king has moved, bother corners in rank 1 are
    no longer available for castling. If the king has not moved,
    and either rook has not moved, then that rook is available for
    castling."""
    if corner not in Square.getCorners():
      return False
    return self._castleFlag[corner]

  def getCastlingOpen(self, kingSquare: Square) -> list:
    """Returns the castling moves that are currently possible"""
    corners = [c for c in Square.getCorners() if c.y == kingSquare.y]
    if not corners:
      return []
    allowCorners = [c for c in corners if c in self.getCastlingFlag(c)]
    if not allowCorners:
      return []

  def clearPosition(self) -> NoReturn:
    """Clears the position by setting all squares to empty"""
    for square in Square:
      self.setPiece(square, ChessPiece.EMPTY)

  def updatePositionFromList(self, positionList: PositionList) -> NoReturn:
    """Updates the position from the list """
    self.clearPosition()
    for line in positionList:
      square = Square.fromStr(line[0])
      piece = ChessPiece.fromColorPiece(line[1], line[2])
      self[square] = piece

  def resetInitialPosition(self) -> NoReturn:
    """Resets the board to initial position"""
    self.updatePositionFromList(initialPosition)

  def emptySquares(self, squares: list[Square]) -> bool:
    """Checks that given list of squares are all empty"""
    if isinstance(squares, list):
      if any([self.getPiece(s) for s in squares]):
        return False
      return True
    msg = """Expected squares to be of type %s, but received %s."""
    raise TypeError(msg % (list, type(squares)))

  def lineOfSight(self, source: Square, target: Square) -> bool:
    """Checks if there is an uninterrupted path between the pieces."""
    squares = []
    if source is target:
      return True  # puts the piece back
    if source | target:  # Indicates that source and target shares file
      d = abs(source.rank - target.rank)
      if d == 1:
        return True
      file = source.file
      rank0 = min(source.rank, target.rank)
      for i in range(1, d):
        squares.append(Square.fromInts(file, rank0 + i))
      return self.emptySquares(squares)
    if source >> target:  # Indicates right moving diagonal
      df, dr = (source.file - target.file), (source.rank - target.rank)
      if (dr / df) ** 2 > 0:
        msg = """Expected squares to be on a diagonal indicated by a slope 
        with absolute value of unity, but received: %.3f ranks per files!"""
        raise UnexpectedStateError(monoSpace(msg), dr / df)
      if dr + df:
        msg = """Expected squares to be on a right moving diagonal, 
        but received a positive slope indicating a left moving diagonal."""
        raise UnexpectedStateError(monoSpace(msg), dr / df)
      d = abs(dr)
      if abs(dr) == 1:
        return True
      file0 = min(source.file, target.file)
      rank0 = max(source.rank, target.rank)
      for i in range(1, d):
        squares.append(Square.fromInts(file0 + i, rank0 - i))
      return self.emptySquares(squares)
    if source << target:  # Indicates left moving diagonal
      df, dr = (source.file - target.file), (source.rank - target.rank)
      if (dr / df) ** 2 > 0:
        msg = """Expected squares to be on a diagonal indicated by a slope 
        with absolute value of unity, but received: %.3f ranks per files!"""
        raise UnexpectedStateError(monoSpace(msg), dr / df)
      if df - dr:
        msg = """Expected squares to be on a left moving diagonal, 
        but received a negative slope indicating a right moving diagonal."""
        raise UnexpectedStateError(monoSpace(msg), dr / df)
      d = abs(dr)
      if abs(dr) == 1:
        return True
      file0 = min(source.file, target.file)
      rank0 = min(source.rank, target.rank)
      for i in range(1, d):
        squares.append(Square.fromInts(file0 + i, rank0 + i))
      return self.emptySquares(squares)
    if source - target:  # Indicates that source and target shares rank
      d = abs(source.file - target.file)
      if d == 1:
        return True
      rank0 = source.rank
      file0 = min(source.rank, target.rank)
      for i in range(1, d):
        squares.append(Square.fromInts(file0 + i, rank0))
      return self.emptySquares(squares)
    return False
