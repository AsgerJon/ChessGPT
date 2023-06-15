"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn
from warnings import warn

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.core import plenty
from worktoy.parsing import maybeTypes
from worktoy.stringtools import stringList, monoSpace
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, PieceMove, File, ChessColor, \
  Rank, PieceType
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
    self._enPassantDebugAllowFlag = False
    self._castleFlag = {s: True for s in Square.getCorners()}

  def setEnPassantDebugAllowFlag(self, flag: bool) -> NoReturn:
    """Setter-function for the en passant override flag"""
    self._enPassantDebugAllowFlag = True if flag else False

  def getEnPassantDebugAllowFlag(self, ) -> bool:
    """Getter-function for the en passant override flag"""
    return self._enPassantDebugAllowFlag

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

  def getAllowEnPassant(self, *args, **kwargs) -> bool:
    """This method controls whether en passant is available. The square
    indicated by arguments are the square occupied by the piece that
    might be captured."""
    square = Square.parse(*args, **kwargs)
    file, rank = square.file, square.rank
    msg = """The pawn at file %s and color %s asked for permission to en 
    passant capture, but en passant is not yet implemented! During 
    development the enPassantDebugAllowFlag decides if en passant is 
    available."""
    warn(msg % (file, rank))
    return self.getEnPassantDebugAllowFlag()

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

  def getPawnMoves(self, square: Square) -> list[Square]:
    """Getter-function for pawn moves matching the color at the given
    square. """
    piece, out = self.getPiece(square), []
    color, square, x, y = piece.color, square.file, square.x, square.y
    if not piece:
      return []
    if color is ChessColor.BLACK:
      if 0 < y < 7:
        oneStepSquare = Square.fromInts(x, y + 1)
        oneStepTarget = self.getPiece(oneStepSquare)
        if oneStepTarget is ChessPiece.EMPTY:
          out.append(oneStepSquare)
          if y == 1:
            twoStepSquare = Square.fromInts(x, y + 2)
            twoStepTarget = self.getPiece(twoStepSquare)
            if twoStepTarget is ChessPiece.EMPTY:
              out.append(twoStepSquare)
        if x < 7:
          plusSquare = Square.fromInts(x + 1, y + 1)
          plusEnPassant = self.getAllowEnPassant(x + 1, y)
          plusCapture = self.getPiece(plusSquare)
          if plusCapture is not ChessPiece.EMPTY or plusEnPassant:
            if plusCapture.color is not color:
              out.append(plusSquare)
        if 0 < x:
          minusSquare = Square.fromInts(x - 1, y + 1)
          minusEnPassant = self.getAllowEnPassant(x - 1, y)
          minusCapture = self.getPiece(minusSquare)
          if minusCapture is not ChessPiece.EMPTY or minusEnPassant:
            if minusCapture.color is not color:
              out.append(minusSquare)
    if color is ChessColor.WHITE:
      if 0 < y < 7:
        oneStepSquare = Square.fromInts(x, y - 1)
        oneStepTarget = self.getPiece(oneStepSquare)
        if oneStepTarget is ChessPiece.EMPTY:
          out.append(oneStepSquare)
          if y == 6:
            twoStepSquare = Square.fromInts(x, y - 2)
            twoStepTarget = self.getPiece(twoStepSquare)
            if twoStepTarget is ChessPiece.EMPTY:
              out.append(twoStepSquare)
        if x < 7:
          plusSquare = Square.fromInts(x + 1, y - 1)
          plusCapture = self.getPiece(plusSquare)
          if plusCapture is not ChessPiece.EMPTY:
            if plusCapture.color is not color:
              out.append(plusSquare)
        if 0 < x:
          minusSquare = Square.fromInts(x - 1, y - 1)
          minusCapture = self.getPiece(minusSquare)
          if minusCapture is not ChessPiece.EMPTY:
            if minusCapture.color is not color:
              out.append(minusSquare)
    return out

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

  def getMoves(self, square) -> list[Square]:
    """Getter-function for the squares that may be captured by the piece
    currently at the given square"""
    piece, out = self.getPiece(square), []
    if not piece:
      return []
    if piece in PieceType.PAWN:
      return self.getPawnMoves(square)
    for move in PieceMove.getTypeMoves(piece.piece):
      target = square + move
      if target is not None:
        if self.captureCheck(piece, target):
          if self.lineOfSight(square, target):
            out.append(target)
    return [s for s in out if s is not square]

  def captureCheck(self, chessPiece: ChessPiece, target: Square) -> bool:
    """Checks if given chess piece can capture the given target square. If
    the target already holds a piece of the same color, the check fails."""
    return False if self.getPiece(target).color == chessPiece.color else True
