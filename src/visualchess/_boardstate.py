"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.core import plenty, maybe
from worktoy.parsing import maybeTypes, maybeType
from worktoy.stringtools import stringList, monoSpace
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, ChessColor, Rank, File, \
  PieceType, Castle
from visualchess._boardstateproperties import _BoardStateProperties
from visualchess.chesspieces import initialPosition

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)
PositionList = list[list[str]]
AllColor = list[tuple[Square, ChessPiece]]
debugPosition = [
  stringList('E8, black, king'),
  stringList('E1, white, king'),
]


class BoardState(_BoardStateProperties):
  """BoardState represents a chess board with each squared occupied by a
  member, possibly the empty one, of the Piece Enum."""

  _whitePawnMoves = [(0, -1), (-1, -1), (1, -1), (0, -2)]
  _blackPawnMoves = [(0, 1), (-1, 1), (1, 1), (0, 2)]

  @staticmethod
  def sign(n: int) -> int:
    """Implementation of signum. 0 is returned for 0."""
    return 0 if not n else (1 if n > 0 else -1)

  @classmethod
  def getWhitePawnMoves(cls) -> list[tuple[int, int]]:
    """Getter-function for white pawn moves"""
    return cls._whitePawnMoves

  @classmethod
  def getBlackPawnMoves(cls) -> list[tuple[int, int]]:
    """Getter-function for black pawn moves"""
    return cls._blackPawnMoves

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
    return cls.readList([
      stringList('E1, white, king'),
      stringList('E8, black, king'),
    ])

  def __init__(self, *args, **kwargs) -> None:
    _BoardStateProperties.__init__(self)

  def getColorKingMoved(self, color: str | ChessColor) -> bool:
    """Getter-function for the moved flag of the king with color as
    indicated"""
    if isinstance(color, str):
      if color in stringList('white, light'):
        return self.getColorKingMoved(ChessColor.WHITE)
      if color in stringList('black, dark'):
        return self.getColorKingMoved(ChessColor.BLACK)
      msg = """%s was not recognized as the name of a chess color!"""
      raise NameError(monoSpace(msg) % color)
    if color is ChessColor.BLACK:
      return self.blackKingMoved
    if color is ChessColor.WHITE:
      return self.whiteKingMoved

  def getColorKingSquare(self, chessColor: ChessColor) -> Square:
    """Getter-function for the square occupied by the king of the given
    color"""
    for square in Square:
      piece = self.getPiece(square)
      if piece.piece is PieceType.KING and piece.color is chessColor:
        return square
    return Square.NULL

  def getPiece(self, *args) -> ChessPiece:
    """Getter-function for the piece on the given square"""
    square = maybeType(Square, *args)
    file = maybeType(File, *args)
    rank = maybeType(Rank, *args)
    if isinstance(file, File) and isinstance(rank, Rank):
      square = maybe(square, Square.fromFileRank(file, rank), Square.NULL)
    if not square:
      return ChessPiece.EMPTY
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
    self._enPassant = Square.NULL

  def delPiece(self, square: Square) -> ChessPiece:
    """Deleter-function for the given square. This removes the piece from
    it. Invoking the deleter returns the chess piece"""
    piece = self.getPiece(square)
    self.setPiece(square, ChessPiece.EMPTY)
    return piece

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
    self.colorTurn = ChessColor.WHITE
    self.updatePositionFromList(initialPosition)

  def leaveBoard(self, ) -> NoReturn:
    """Resets move properties"""
    self.hoverPiece = ChessPiece.EMPTY
    self.hoverSquare = Square.NULL
    self.cancelMove()

  def hover(self, square: Square) -> NoReturn:
    """Sets hoverSquare to square"""
    piece = self.getPiece(square)
    if self.hoverSquare != square:
      self.hoverSquare = square
    if self.hoverPiece != self.getPiece(square):
      self.hoverPiece = piece

  def grabPiece(self, ) -> NoReturn:
    """Grabs the hovered piece"""
    if self.hoverPiece.color == self.colorTurn:
      if self.hoverPiece and self.hoverSquare:
        self.grabbedPiece = self.hoverPiece
        self.grabbedSquare = self.hoverSquare
        self.delPiece(self.grabbedSquare)
        return True
    return False

  def cancelMove(self, ) -> NoReturn:
    """This method instead moves the grabbed piece back to grabbed square"""
    if self.grabbedPiece and self.grabbedSquare:
      self.setPiece(self.grabbedSquare, self.grabbedPiece)
      self.soundCancelMove.play()
    self.grabbedSquare, self.grabbedPiece = Square.NULL, ChessPiece.EMPTY

  def moveVector(self, ) -> tuple[int, int]:
    """Returns the vector like object spanning from grabbed to hover
    squares. Positive direction indicate the direction moved by black
    pawns and from file A towards file H."""
    if not (self.grabbedSquare and self.grabbedSquare):
      return (0, 0)
    file0, rank0 = self.grabbedSquare.file, self.grabbedSquare.rank
    file1, rank1 = self.hoverSquare.file, self.hoverSquare.rank
    return (file1.value - file0.value, rank1.value - rank0.value)

  def validateBase(self) -> tuple[int, int]:
    """Base validation"""
    if self.hoverPiece:
      if self.hoverPiece.color == self.grabbedPiece.color:
        self.soundIllegalCapture.play()
        return (0, 0)
    if self.hoverSquare == self.grabbedSquare:
      return (0, 0)
    if not self.grabbedPiece:
      return (0, 0)
    supremum = self.grabbedSquare - self.hoverSquare
    infimum = self.grabbedSquare * self.hoverSquare
    if isinstance(supremum, int) and isinstance(infimum, int):
      return (supremum, infimum)

  def validateKnightMove(self) -> bool:
    """Validates a knight move"""
    supremum, infimum = self.validateBase()
    if not supremum * infimum:
      return False
    if self.grabbedPiece.isKnight:
      if supremum == 2 and infimum == 1:
        return True
      return False

  def validateRanged(self) -> bool:
    """Validates a ranged move"""
    sign = lambda arg: (1 if arg > 0 else -1) if arg else 0
    x0, x1 = self.grabbedSquare.file.value, self.hoverSquare.file.value
    y0, y1 = self.grabbedSquare.rank.value, self.hoverSquare.rank.value
    dx, dy = x1 - x0, y1 - y0
    c = 1
    while c < 7:
      x, y = x0 + c * sign(dx), y0 + c * sign(dy)
      if self.hoverSquare.file.value == x:
        if self.hoverSquare.rank.value == y:
          return True
      square = Square.fromInts(x, y)
      if self.getPiece(square):
        return False
      c += 1

  def validateKingMove(self) -> bool:
    """Validates a king move"""
    x0, x1 = self.grabbedSquare.file.value, self.hoverSquare.file.value
    y0, y1 = self.grabbedSquare.rank.value, self.hoverSquare.rank.value
    if max(x1 - x0, y1 - y0) < 2:
      return True
    return False

  def validateShortCastleWhite(self) -> bool:
    """Validates short castling for king. Does not yet validate if the
    king is in check."""
    if self.whiteKingMoved or self.whiteRookHMoved:
      return False
    if self.getPiece(Square.fromFileRank(File.F, Rank.rank1)):
      return False
    if self.getPiece(Square.fromFileRank(File.G, Rank.rank1)):
      return False
    return True

  def squaresPiecesColor(self, chessColor: ChessColor) -> AllColor:
    """Returns a list of tuples with square and piece where the piece is
    of the color indicated."""
    out = []
    for square in Square:
      piece = self.getPiece(square)
      if piece:
        if piece.color is chessColor:
          out.append((square, piece))
    return out

  def getColorReach(self, chessColor: ChessColor) -> list[Square]:
    """Getter-function for all squares reachable by a piece of the given
    color"""
    out, sourceSquare, sourcePiece = [], None, None
    colorSquares = self.squaresPiecesColor(chessColor)
    for (sourceSquare, sourcePiece) in colorSquares:
      for targetSquare in Square:
        if sourceSquare is not targetSquare:
          targetPiece = self.getPiece(targetSquare)
          if self.validateMove(
              sourceSquare, targetSquare, sourcePiece, targetPiece):
            out.append(targetSquare)
    return out

  def colorKingCheck(self, *args) -> bool:
    """Getter-function for flag indicating that the king of the given
    color is in check"""
    chessColor = maybeType(ChessColor, *args)
    if not isinstance(chessColor, ChessColor):
      raise TypeError
    square = maybeType(Square, *args)
    square = maybe(square, self.getColorKingSquare(chessColor))
    if chessColor is ChessColor.NULL:
      raise ValueError('NULL color has no king!')
    otherColorReach = self.getColorReach(~chessColor)
    return True if square in otherColorReach else False

  def whiteShortCastle(self) -> bool:
    """Validates if the white king may castle short"""
    if self.whiteKingMoved or self.whiteRookHMoved:
      return False
    blackReach = self.getColorReach(ChessColor.BLACK)
    squares = [Square.fromFileRank(f, Rank.rank1) for f in [File.F, File.G]]
    if any([s in blackReach for s in squares]):
      return False
    if any([self.getPiece(square) for square in squares]):
      return False
    return True

  def validateCastlingHasMoved(self, color: str, direction: str) -> bool:
    """Checks if indicated castling operation is prevented by the relevant
    king or rook has already moved."""
    castle = Castle.fromStr(color, direction)
    if self.getColorKingMoved(castle.color):
      return False
    if castle.color is ChessColor.BLACK:
      if castle.direction == 'short':
        if self.blackRookHMoved:
          return False
      if castle.direction == 'long':
        if self.blackRookAMoved:
          return False
    if castle.color is ChessColor.WHITE:
      if castle.direction == 'short':
        if self.whiteRookHMoved:
          return False
      if castle.direction == 'long':
        if self.whiteRookAMoved:
          return False
    return True

  def validateCastlingStepSquares(self, color: str, direction: str) -> bool:
    """Checks if the stepSquares are empty"""
    castle = Castle.fromStr(color, direction)
    for square in castle.squares:
      if self.getPiece(square):
        return False
    return True

  def validateCastlingCheck(self, color: str, direction: str) -> bool:
    """Checks if the relevant king is being checked or would be checked
    during the castle move"""
    castle = Castle.fromStr(color, direction)
    otherReach = self.getColorReach(~castle.color)
    for square in castle.squares:
      if square in otherReach:
        return False
    return True

  def parseSquares(self, *squares: Square) -> tuple[Square, Square]:
    """Parses positional arguments to instances of Squares. If only one
    square is given explicitly, it is ignored and replaced by the default
    values which are the grabbed square and the hover square"""
    sourceSquare, targetSquare = self.grabbedSquare, self.hoverSquare
    squares = maybeTypes(Square, *squares, padLen=2, padChar=None)
    source = maybe(sourceSquare, squares[0])
    target = maybe(sourceSquare, squares[1])
    if isinstance(source, Square) and isinstance(target, Square):
      return (source, target)
    sourceMsg, targetMsg = '', ''
    if not isinstance(source, Square):
      sourceMsg = """Expected 'source' argument to be of type %s, 
      but received %s of type %s!""" % (Square, source, type(source))
    if not isinstance(target, Square):
      targetMsg = """Expected 'target' argument to be of type %s, 
      but received %s of type %s""" % (Square, target, type(target))
    if targetMsg and sourceMsg:
      msg = 'Encountered the following errors:\n%s\n%s'
      raise TypeError(msg % (sourceMsg, targetMsg))
    if targetMsg:
      raise TypeError(targetMsg)
    if sourceMsg:
      raise TypeError(sourceMsg)
    raise UnexpectedStateError('Unexpected state encountered!')

  def rangedLike(self, *squares) -> list[Square]:
    """Determines if a bishop would be able to move between the squares
    given. Returns a list, possibly empty, of the squares separating the
    squares. For squares that a bishop cannot traverse and a list with the
    NULL square is returned."""
    source, target = self.parseSquares(*squares)
    x0, x1 = source.file.value, target.file.value
    y0, y1 = source.rank.value, target.rank.value
    if abs(x1 - x0) - abs(y1 - y0):  # excludes bishops
      if abs(x1 - x0) + abs(y1 - y0):  # excludes rooks
        return [Square.NULL]
    if -2 < (x1 - x0) * (y1 - y0) < 2:
      return []
    x0, x1 = source.file.value, target.file.value
    y0, y1 = source.rank.value, target.rank.value
    dx, dy, out = self.sign(x1 - x0), self.sign(y1 - y0), []
    for i in range(1, abs(x1 - x0)):
      out.append(Square.fromInts(x0 + i * dx, y0 + i * dy))
    return out

  def knightLike(self, *squares) -> bool:
    """Checks if a knight could jump between the two squares given."""
    source, target = self.parseSquares(*squares)
    dFile = abs(target.file.value - source.file.value)
    dRank = abs(target.rank.value - source.rank.value)
    if min(dFile, dRank) == 1 and max(dFile, dRank) == 2:
      return True
    return False

  def kingLike(self, *squares) -> bool:
    """Checks if king could move between the two squares given."""
    source, target = self.parseSquares(*squares)
    dFile = abs(target.file.value - source.file.value)
    dRank = abs(target.rank.value - source.rank.value)
    return True if max(dFile, dRank) < 2 else False

  def whitePawnLike(self, *squares) -> list[Square]:
    """Checks if a white pawn could traverse the squares given. For this
    particular case, take not that the order matters with the source
    square coming first."""
    source, target = self.parseSquares(*squares)
    x0, x1 = source.file.value, target.file.value
    y0, y1 = source.rank.value, target.rank.value
    if y0 - y1 not in [1, 2]:
      return [Square.NULL]
    if (x0 - x1) ** 2 > 1:
      return [Square.NULL]
    if y0 - y1 == 2 and (x0 - x1 or y0 != 6):
      return [Square.NULL]
    if abs(y1 - y0) == 1:
      return []
    if abs(y1 - y0) == 2:
      return [Square.fromInts(x0, 6)]
    raise UnexpectedStateError('Pawn squares')

  def blackPawnLike(self, *squares) -> list[Square]:
    """For black pawn. See docstring above."""
    source, target = self.parseSquares(*squares)
    x0, x1 = source.file.value, target.file.value
    y0, y1 = source.rank.value, target.rank.value
    if y1 - y0 not in [1, 2]:
      return [Square.NULL]
    if (x1 - x0) ** 2 > 1:
      return [Square.NULL]
    if y1 - y0 == 2 and (x1 - x0 or y0 != 1):
      return [Square.NULL]
    if abs(y1 - y0) == 1:
      return []
    if abs(y1 - y0) == 2:
      return [Square.fromInts(x0, 1)]
    raise UnexpectedStateError('Pawn squares')

  def validateMove(self, *args) -> bool:
    """This method checks if moving grabbed Piece to hoverSquare is
    allowable."""
    sourceSquare, targetSquare = self.parseSquares(*args)
    sourcePiece, targetPiece = maybeTypes(ChessPiece, *args)
    if not plenty(sourcePiece, targetPiece):
      sourcePiece, targetPiece = self.grabbedPiece, self.hoverPiece
    if not isinstance(sourceSquare, Square):
      raise TypeError
    if not isinstance(targetSquare, Square):
      raise TypeError
    if not isinstance(sourcePiece, ChessPiece):
      raise TypeError
    if not isinstance(targetPiece, ChessPiece):
      raise TypeError
    if sourcePiece is ChessPiece.EMPTY:
      msg = """The source piece must not be the empty piece!"""
      raise ValueError(msg)
    if targetPiece is not ChessPiece.EMPTY:
      if sourcePiece.color is targetPiece.color:
        return False
    if sourcePiece.isKnight or sourcePiece.isKing:
      return True
    stepSquares = [777]
    if sourcePiece.isRanged:
      stepSquares = self.rangedLike(sourceSquare, targetSquare)
    if sourcePiece.isPawn:
      if sourcePiece.isWhite:
        stepSquares = self.whitePawnLike(sourceSquare, targetSquare)
      if sourcePiece.isBlack:
        stepSquares = self.blackPawnLike(sourceSquare, targetSquare)
    for square in stepSquares:
      if square == 777:
        raise UnexpectedStateError('step squares validation')
      if square is Square.NULL:
        return False
      if self.getPiece(square) is not ChessPiece.EMPTY:
        return False
    return True

  def applyMove(self, ) -> NoReturn:
    """Moves grabbed piece to the hovered square if validated."""
    if self.validateMove():
      if self.hoverPiece:
        self.soundAllowedCapture.play()
      self.setPiece(self.hoverSquare, self.grabbedPiece)
      self.grabbedPiece = ChessPiece.EMPTY
      self.grabbedSquare = Square.NULL
      self.toggleTurn()
      self.soundAllowedMove.play()
      return True
    self.cancelMove()
    return False

  def _getMoves(self) -> list:
    """Getter-function for all available moves. """

  def __str__(self) -> str:
    """String Representation"""
    out = ''
    for rank in Rank:
      for file in File:
        piece = self.getPiece(file, rank)
        if not piece:
          out += '__'
