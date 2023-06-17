"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn, Never

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import maybeType, searchKeys
from worktoy.stringtools import stringList, monoSpace
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError, ReadOnlyError

from moreworktoy import ArgumentError
from visualchess import ChessPiece, Square, ChessColor, Rank, PieceType
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
    self._enPassant = Square.NULL
    self._grabbedPiece = ChessPiece.EMPTY
    self._grabbedSquare = Square.NULL
    self._hoverSquare = Square.NULL
    self._hoverPiece = ChessPiece.EMPTY

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

  def _getGrabbedPiece(self) -> ChessPiece:
    """Getter-function for the grabbed piece"""
    return self._grabbedPiece

  def _setGrabbedPiece(self, chessPiece: ChessPiece) -> NoReturn:
    """Setter-function for the grabbed piece"""
    self._grabbedPiece = chessPiece

  def _getGrabbedSquare(self) -> Square:
    """Getter-function for the grabbed square"""
    return self._grabbedSquare

  def _setGrabbedSquare(self, square: Square) -> NoReturn:
    """Setter-function for the hovered square"""
    self._grabbedSquare = square

  def _getHoverSquare(self) -> Square:
    """Getter-function for the grabbed square"""
    return self._hoverSquare

  def _setHoverSquare(self, square: Square) -> NoReturn:
    """Setter-function for the hovered square"""
    self._hoverSquare = square

  def _getHoverPiece(self) -> ChessPiece:
    """Getter-function for the hovered piece"""
    return self._hoverPiece

  def _setHoverPiece(self, chessPiece: ChessPiece) -> NoReturn:
    """Setter-function for the hovered square"""
    self._hoverPiece = chessPiece

  def getPiece(self, *args, **kwargs) -> ChessPiece:
    """Getter-function for the piece on the given square"""
    square = Square.parse(*args, **kwargs)
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
    self.updatePositionFromList(initialPosition)

  def _getEnPassantSquare(self) -> Square:
    """Getter-function for the square, if any, where en passant capture is
    currently possible."""
    if isinstance(self._enPassant, Square):
      return self._enPassant
    msg = """Expected the en-passant square to be of type %s, 
    but received: %s!"""
    raise TypeError(msg % (Square, type(self._enPassant)))

  def _setEnPassantSquare(self, square: Square) -> NoReturn:
    """Setter-function for the en passant square. Please note that this
    setter checks if this square has a pawn on it of the appropriate
    color. If not, it will raise an UnexpectedStateError. To avoid this,
    ensure that the pawn move after which the pawn may be captured with en
    passant is applied to the board state, before the setter function is
    invoked. """
    if not isinstance(square, Square):
      msg = """Expected the en-passant square to be of type %s, 
      but received: %s!"""
      raise TypeError(msg % (Square, type(self._enPassant)))
    if not square:
      self._enPassant = Square.NULL
      return
    piece = self.getPiece(square)
    if piece.piece is not PieceType.PAWN:
      msg = """Expected a piece of type %s at %s, but found %s!"""
      raise TypeError(msg % (PieceType.PAWN, square, piece.piece))
    if piece.color is ChessColor.WHITE and square.rank == 4:
      self._enPassant = square
    elif piece.color is ChessColor.BLACK and square.rank == 3:
      self._enPassant = square
    else:
      msg = """Expected rank of en-passant square to be on %s or %s!"""
      raise ValueError(msg % (Rank.rank4, Rank.rank5, square.rank))

  def parsePos(self, *args) -> tuple[Square, ChessColor, PieceType]:
    """Parses arguments to square and chess piece"""
    square = maybeType(Square, *args)
    chessPieceArg = maybeType(ChessPiece, *args)
    defaultType, defaultColor = None, None
    if chessPieceArg:
      if isinstance(chessPieceArg, ChessPiece):
        defaultType, defaultColor = chessPieceArg.piece, chessPieceArg.color
    pieceTypeArg = maybeType(PieceType, *args)
    colorArg = maybeType(ChessColor, *args)
    pieceType = maybe(pieceTypeArg, defaultType, PieceType.EMPTY)
    color = maybe(colorArg, defaultColor, ChessColor.NULL)
    if isinstance(square, Square):
      if isinstance(color, ChessColor):
        if isinstance(pieceType, PieceType):
          return (square, color, pieceType)

  def parseKey(self, **kwargs) -> tuple[Square, ChessColor, PieceType]:
    """Parses keyword arguments to square and chess piece"""
    squareKeys = stringList('square, position, coordinates, field')
    chessPieceKeys = stringList('chessPiece, piece, pieceType, type, type_')
    colorKeys = stringList('color, colour, chessColor, side')
    squareKwarg = searchKeys(*squareKeys) @ Square >> kwargs
    chessPieceKwarg = searchKeys(*chessPieceKeys) @ ChessPiece >> kwargs
    pieceTypeKwarg = searchKeys(*chessPieceKeys) @ PieceType >> kwargs
    colorKwarg = searchKeys(*colorKeys) @ ChessColor >> kwargs
    square = maybe(squareKwarg, Square.NULL)
    chessPiece = maybe(chessPieceKwarg, ChessPiece.EMPTY)
    defaultType, defaultColor = None, None
    if chessPiece:
      if isinstance(chessPiece, ChessPiece):
        defaultType, defaultColor = chessPiece.piece, chessPiece.color
    pieceType = maybe(pieceTypeKwarg, defaultType, PieceType.EMPTY)
    color = maybe(colorKwarg, defaultColor, ChessColor.NULL)
    if isinstance(square, Square):
      if isinstance(color, ChessColor):
        if isinstance(pieceType, PieceType):
          return (square, color, pieceType)

  def parse(self, *args, **kwargs) -> tuple[Square, ChessColor, PieceType]:
    """Parses arguments to square and piece"""
    posArgs = self.parsePos(*args)
    keyArgs = self.parseKey(**kwargs)
    square = maybe(keyArgs[0], posArgs[0], None)
    color = maybe(keyArgs[1], posArgs[1], None)
    pieceType = maybe(keyArgs[2], posArgs[2], None)
    if isinstance(square, Square):
      if isinstance(color, ChessColor):
        if isinstance(pieceType, PieceType):
          return (square, color, pieceType)

  def squareTargets(self, *args) -> list[Square]:
    """Returns the squares that the piece on the given squares is able to
    move to."""
    square = maybeType(Square, *args)
    chessPiece = maybeType(ChessPiece, *args)
    if not isinstance(chessPiece, ChessPiece):
      raise TypeError
    pieceType = chessPiece.piece
    if pieceType is PieceType.PAWN:
      return self.pawnTargets(square, chessPiece)
    return [square for square in Square]

  def pawnTargets(self, *args) -> list[Square]:
    """Returns the squares reachable by a white pawn from the given square"""
    out = []
    black, white = ChessColor.BLACK, ChessColor.WHITE
    square = maybeType(Square, *args)
    chessPiece = maybeType(ChessPiece, *args)
    if isinstance(chessPiece, ChessPiece):
      color, pieceType = chessPiece.color, chessPiece.piece
    else:
      raise TypeError
    if not isinstance(square, Square):
      raise TypeError
    if not isinstance(chessPiece, ChessPiece):
      raise TypeError
    step = 1 if color is black else -1
    oneStep = square + step * 1j
    if oneStep:
      if not self.getPiece(oneStep):
        out.append(oneStep)
    initialRank = Rank.rank7 if color is black else Rank.rank2
    if square.rank == initialRank:
      twoStep = square + 2j if color is ChessColor.BLACK else square - 2j
      if not (self.getPiece(twoStep) and self.getPiece(oneStep)):
        out.append(twoStep)
    dr = 1j if color is ChessColor.BLACK else -1j
    for step in [-1 + dr, 1 + dr]:
      if square + step:
        colorTest = self.getPiece(square + step).color == ~color
        enPassantTest = square + int(step.real) == self.enPassantSquare
        if colorTest or enPassantTest:
          out.append(square + step)
    return out

  def validateMove(self, ) -> bool:
    """This method should be invoked to apply a move to the board"""
    if not self.grabbedPiece:
      return False
    color = self.grabbedPiece.color
    black, white = ChessColor.BLACK, ChessColor.WHITE
    if self.grabbedPiece.isPawn:
      initialRank = Rank.rank7 if color is black else Rank.rank2
      direction = 1 if color is black else -1
      file0, rank0 = self.grabbedSquare.file, self.grabbedSquare.rank
      file1, rank1 = self.hoverSquare.file, self.hoverSquare.rank
      if direction * (rank1.value - rank0.value) < 0:
        print('Would move pawn backwards')
        return False  # Would move pawn backwards
      if rank1.value - rank0.value == 2 * direction:
        if rank0.value - initialRank.value:
          print('Two steps available only from initial rank')
          return False  # Two steps available only from initial rank
        if file0.value - file1.value:
          print('Two steps must occur on one file')
          return False  # Two steps must occur on one file
        if self.getPiece(Square.fromFileRank(file0, rank0 + direction)):
          print('Two steps obstructed')
          return False  # Two steps obstructed!
        if self.getPiece(Square.fromFileRank(file0, rank0 + 2 * direction)):
          print('Two steps obstructed')
          return False  # Two steps obstructed!
        self._enPassant = self.hoverSquare
        return True
      if rank1.value - rank0.value == direction:
        if file0.value == file1.value:
          if self.getPiece(Square.fromFileRank(file0, rank0 + direction)):
            print('One step obstructed!')
            return False  # One step obstructed!
          return True
        else:
          if max(file0, file1) - min(file0, file1) != 1:
            return False
          if self.hoverPiece.color == color:
            return False
          return True
      dx = self.enPassantSquare.file.value - self.hoverSquare.file.value
      if dx in [-1, 1]:
        return True

  def applyMove(self) -> bool:
    """Applies the current move subject to validation"""
    if self.validateMove():
      self.setPiece(self.hoverSquare, self.grabbedPiece)
      self.grabbedPiece = ChessPiece.EMPTY
      self.grabbedSquare = Square.NULL
      self.hoverPiece = ChessPiece.EMPTY
      self.hoverSquare = Square.NULL
      return True
    return False

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('General illegal accessor')

  enPassantSquare = property(
    _getEnPassantSquare, _setEnPassantSquare, _noAcc)
  grabbedPiece = property(_getGrabbedPiece, _setGrabbedPiece, _noAcc)
  grabbedSquare = property(_getGrabbedSquare, _setGrabbedSquare, _noAcc)
  hoverSquare = property(_getHoverSquare, _setHoverSquare, _noAcc)
  hoverPiece = property(_getHoverPiece, _setHoverPiece, _noAcc)
