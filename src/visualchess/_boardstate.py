"""BoardState represents the chessboard at a given state. Instances are
mutable."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QPixmap
from icecream import ic
from worktoy.core import plenty
from worktoy.parsing import maybeType

from visualchess import ChessColor, Piece, File, Rank, loadPiece

ic.configureOutput(includeContext=True)

white, black = ChessColor.WHITE, ChessColor.BLACK
king, queen, rook = Piece.KING, Piece.QUEEN, Piece.ROOK
bishop, knight, pawn = Piece.BISHOP, Piece.KNIGHT, Piece.PAWN
_A, _B, _C, _D, _E, _F, _G, _H = [file for file in File]
_1, _2, _3, _4, _5, _6, _7, _8 = [rank for rank in Rank]


class ChessPiece:
  """Chess piece represents a chess piece by type and color"""

  _NULL = None

  @classmethod
  def _checkNullPieceExists(cls) -> bool:
    """Checks if the null chess piece has been created"""
    return True if cls._NULL is None else False

  @classmethod
  def _createNullPiece(cls) -> NoReturn:
    """Creates a null piece"""
    cls._NULL = ChessPiece(null=True)
    setattr(cls._NULL, '__NULL__', True)

  @classmethod
  def _getNullPiece(cls) -> ChessPiece:
    """Getter-function for the null piece"""
    if cls._NULL is None:
      cls._createNullPiece()
      return cls._getNullPiece()
    return cls._NULL

  @classmethod
  def parseArgs(cls, *args) -> ChessPiece:
    """Parses arguments"""
    chessPiece = maybeType(ChessPiece, *args)
    if isinstance(chessPiece, ChessPiece):
      return chessPiece
    piece = maybeType(Piece, *args)
    color = maybeType(ChessColor, *args)
    if isinstance(piece, Piece) and isinstance(color, ChessColor):
      return ChessPiece(piece, color)
    return cls._getNullPiece()

  def __init__(self, *args, **kwargs) -> None:
    self._piece = maybeType(Piece, *args)
    self._color = maybeType(ChessColor, *args)
    self._file = maybeType(File, *args)
    self._rank = maybeType(Rank, *args)
    if not plenty(self._piece, self._color, self._file, self._rank):
      if not kwargs.get('null', False) and not self._checkNullPieceExists():
        raise TypeError

  def __eq__(self, other: ChessPiece) -> bool:
    """Piece and color must be the same. The NULL ChessPiece is not equal
    to itself"""
    if getattr(self, '__NULL__', False) or getattr(other, '__NULL__', False):
      return False
    if self._color != other._color:
      return False
    if self._piece != other._piece:
      return False
    return True

  def getFile(self) -> File:
    """Getter-function for hte current file the piece occupies"""
    if isinstance(self._file, File):
      return self._file

  def setFile(self, file: File) -> NoReturn:
    """Setter-function for hte current file the piece occupies"""
    if isinstance(file, File):
      self._file = file

  def getRank(self) -> Rank:
    """Getter-function for the current rank the piece occupies"""
    if isinstance(self._rank, Rank):
      return self._rank

  def setRank(self, rank: Rank) -> NoReturn:
    """Getter-function for the current rank the piece occupies"""
    if isinstance(rank, Rank):
      self._rank = rank

  def getColor(self) -> ChessColor:
    """Getter-function for color"""
    if isinstance(self._color, ChessColor):
      return self._color

  def getPiece(self) -> Piece:
    """Getter-function for color"""
    if isinstance(self._piece, Piece):
      return self._piece

  def getPixmap(self) -> QPixmap:
    """Loads pixmap representation of this instance"""
    return loadPiece(self.getPiece(), self.getColor())

  def __str__(self) -> str:
    """String representation"""
    colorString = '%s' % self.getColor()
    pieceString = '%s' % self.getPiece()
    return '%s %s' % (colorString, pieceString)

  def __repr__(self, ) -> str:
    """Code Representation"""
    colorCode = '%s' % (self.getColor().__repr__())
    pieceCode = '%s' % (self.getPiece().__repr__())
    return 'BoardState(%s, %s)' % (colorCode, pieceCode)


class Square:
  """Class defining individual squares on the board"""

  _NULL = None

  @classmethod
  def _createNULL(cls) -> NoReturn:
    """Creator-function for the null square"""
    cls._NULL = cls(File.byValue(0), Rank.byValue(0))
    setattr(cls._NULL, '_file', None)
    setattr(cls._NULL, '_rank', None)
    setattr(cls._NULL, '__NULL__', True)

  @classmethod
  def getNULL(cls) -> Square:
    """Getter-function for the null square"""
    if cls._NULL is None:
      cls._createNULL()
      return cls.getNULL()
    return cls._NULL

  @classmethod
  def parseArgs(cls, *args) -> tuple[File, Rank] | Square:
    """Parses arguments to square"""
    square = maybeType(Square, *args)
    if isinstance(square, Square):
      return square
    else:
      file = maybeType(File, *args)
      rank = maybeType(Rank, *args)
      if isinstance(file, File) and isinstance(rank, Rank):
        return Square(file, rank)

  @classmethod
  def int2Square(cls, num: int) -> Square:
    """Getter-function for the square at the given index"""
    rank = Rank.byValue(num % 8)
    file = File.byValue(num // 8)
    if isinstance(file, File) and isinstance(rank, Rank):
      return Square(file, rank)

  def __new__(cls, *args) -> Square:
    """Throws the NULL square where appropriate"""
    file = maybeType(File, *args)
    rank = maybeType(Rank, *args)
    if plenty(file, rank):
      return super().__new__(cls)
    return cls.getNULL()

  def __init__(self, *args) -> None:
    file = maybeType(File, *args)
    rank = maybeType(Rank, *args)
    self._file = None
    self._rank = None
    if isinstance(file, File):
      self._file = file
    if isinstance(rank, Rank):
      self._rank = rank
    if not plenty(self._file, self._rank):
      raise TypeError
    self._piece = None

  def getFile(self) -> File:
    """Getter-function for hte current file the piece occupies"""
    if isinstance(self._file, File):
      return self._file

  def getRank(self) -> Rank:
    """Getter-function for the current rank the piece occupies"""
    if isinstance(self._rank, Rank):
      return self._rank

  def __hash__(self, ) -> int:
    """Hashing"""
    if getattr(self, '__NULL__', False):
      return -1
    return self.getFile().value * 8 + self.getRank().value

  def __bool__(self) -> bool:
    """Always True except for NULL square"""
    return False if getattr(self, '__NULL__', False) else True

  def __eq__(self, other: Square) -> bool:
    """Equality operator"""
    if self and other:
      if self.getFile() != other.getFile():
        return False
      if self.getRank() != other.getRank():
        return False
      return True
    return False

  def __str__(self, ) -> str:
    """String Representation"""
    fileString = '%s' % self.getFile()
    rankString = '%s' % self.getRank()
    return '%s%s' % (fileString, rankString)

  def __repr__(self, ) -> str:
    """Code Representation"""
    fileCode = self.getFile().__repr__()
    rankCode = self.getRank().__repr__()
    return 'Square(%s, %s)' % (fileCode, rankCode)


class BoardState:
  """BoardState represents the chessboard at a given state. Instances are
  mutable.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    self.__index__ = 0
    self._contents = {}
    self._initContents()
    self._setPiece(_A, _1, white, rook)
    self._setPiece(_A, _2, white, pawn)
    self._setPiece(_A, _7, black, pawn)
    self._setPiece(_A, _8, black, rook)
    self._setPiece(_B, _1, white, knight)
    self._setPiece(_B, _2, white, pawn)
    self._setPiece(_B, _7, black, pawn)
    self._setPiece(_B, _8, black, knight)
    self._setPiece(_C, _1, white, bishop)
    self._setPiece(_C, _2, white, pawn)
    self._setPiece(_C, _7, black, pawn)
    self._setPiece(_C, _8, black, bishop)
    self._setPiece(_D, _1, white, queen)
    self._setPiece(_D, _2, white, pawn)
    self._setPiece(_D, _7, black, pawn)
    self._setPiece(_D, _8, black, queen)
    self._setPiece(_E, _1, white, king)
    self._setPiece(_E, _2, white, pawn)
    self._setPiece(_E, _7, black, pawn)
    self._setPiece(_E, _8, black, king)
    self._setPiece(_F, _1, white, bishop)
    self._setPiece(_F, _2, white, pawn)
    self._setPiece(_F, _7, black, pawn)
    self._setPiece(_F, _8, black, bishop)
    self._setPiece(_G, _1, white, knight)
    self._setPiece(_G, _2, white, pawn)
    self._setPiece(_G, _7, black, pawn)
    self._setPiece(_G, _8, black, knight)
    self._setPiece(_H, _1, white, rook)
    self._setPiece(_H, _2, white, pawn)
    self._setPiece(_H, _7, black, pawn)
    self._setPiece(_H, _8, black, rook)

  def _initContents(self) -> NoReturn:
    """Initialises the content dictionary"""
    for file in File:
      for rank in Rank:
        square = Square(file, rank)
        self._contents |= {square: None}

  def _setPiece(self, *args) -> NoReturn:
    """Setter-function for the square and piece"""
    square = Square.parseArgs(*args)
    piece = ChessPiece.parseArgs(*args)
    self._contents |= {square: piece}

  def squareStatus(self, *args) -> ChessPiece:
    """Use instances of Square as keys"""
    square = Square.parseArgs(*args)
    return self._contents.get(square, Square)

  def setSquarePiece(self, *args) -> NoReturn:
    """Setter-function for the piece and square given"""
    square = Square.parseArgs(*args)
    self._contents[square] = ChessPiece.parseArgs(*args)

  def clearSquarePiece(self, *args) -> NoReturn:
    """Clear-function for the square"""
    square = Square.parseArgs(*args)
    self._contents[square] = None

  def getContents(self) -> dict[Square, ChessPiece]:
    """Getter-function for contents library"""
    return self._contents
