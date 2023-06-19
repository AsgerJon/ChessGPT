"""_BoardStateProperties is the properties class used by BoardState"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Never

from icecream import ic
from worktoy.core import maybe
from worktoy.waitaminute import ReadOnlyError

from visualchess import ChessAudio, Square, ChessPiece, ChessColor, Move, \
  File

ic.configureOutput(includeContext=True)


class _BoardStateProperties(ChessAudio):
  """_BoardStateProperties is the properties class used by BoardState
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessAudio.__init__(self)
    self._contents = {s: ChessPiece.EMPTY for s in Square}
    self._colorTurn = ChessColor.WHITE
    self._enPassant = Square.NULL
    self._grabbedPiece = ChessPiece.EMPTY
    self._grabbedSquare = Square.NULL
    self._hoverSquare = Square.NULL
    self._hoverPiece = ChessPiece.EMPTY
    self._whiteKingHasMoved = False
    self._blackKingHasMoved = False
    self._whiteRookAHasMoved = False
    self._whiteRookHHasMoved = False
    self._blackRookAHasMoved = False
    self._blackRookHHasMoved = False

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

  def _getGrabbedColor(self) -> ChessColor:
    """Getter-function for the color of the grabbed piece"""
    return self.grabbedPiece.color

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

  def _getHoverColor(self) -> ChessColor:
    """Getter-function for the color of the hovered piece"""
    return self.hoverPiece.color

  def _getTurn(self) -> ChessColor:
    """Getter-function for the color whose turn it is."""
    return self._colorTurn

  def _setTurn(self, chessColor: ChessColor) -> NoReturn:
    """Setter-function for the color whose turn it is."""
    self._colorTurn = chessColor

  def _getEnPassantFile(self, ) -> File:
    """Getter-function for the current en passant file. Please note the
    use of 'File.NULL' indicating that no en passant move is possible."""
    file = maybe(self._enPassant, File.NULL)
    if isinstance(file, File):
      self._enPassant = File.NULL
      return file
    raise TypeError

  def _setEnPassantFile(self, file: File = None) -> NoReturn:
    """Setter-function for the current en passant file."""
    file = maybe(file, File.NULL)
    if isinstance(file, File):
      self._enPassant = file
    else:
      raise TypeError

  def toggleTurn(self) -> NoReturn:
    """Toggle-function switching the turn"""
    if self._colorTurn is ChessColor.BLACK:
      self._colorTurn = ChessColor.WHITE
    else:
      self._colorTurn = ChessColor.BLACK

  def _getHoverTurn(self, ) -> bool:
    """Getter-function for hover turn flag. True indicates that the piece
    currently hovered is of the color whose turn it is."""
    if not self.hoverPiece:
      return False
    if self.hoverPiece.color == self.colorTurn:
      return True
    return False

  def _getWhiteKingMovedFlag(self) -> bool:
    """Getter-function for the white king move flag"""
    return self._whiteKingHasMoved

  def _setWhiteKingMovedFlag(self, *_) -> NoReturn:
    """Single shot setter function for the white king move flag"""
    self._whiteKingHasMoved = False

  def _getBlackKingMovedFlag(self) -> bool:
    """Getter-function for the black king move flag"""
    return self._blackKingHasMoved

  def _setBlackKingMovedFlag(self, *_) -> NoReturn:
    """Single shot setter function for the black king move flag"""
    self._blackKingHasMoved = True

  def _getBlackRookAMovedFlag(self) -> bool:
    """Single shot getter function for the black rook on file A move flag"""
    return self._blackRookAHasMoved

  def _setBlackRookAMovedFlag(self, *_) -> NoReturn:
    """Single shot setter function for the black rook on file A move flag"""
    self._blackRookAHasMoved = True

  def _getBlackRookHMovedFlag(self) -> bool:
    """Single shot getter function for the black rook on file H move flag"""
    return self._blackRookHHasMoved

  def _setBlackRookHMovedFlag(self, *_) -> NoReturn:
    """Single shot setter function for the black rook on file H move flag"""
    self._blackRookHHasMoved = True

  def _getWhiteRookAMovedFlag(self) -> bool:
    """Single shot getter function for the white rook on file A move flag"""
    return self._whiteRookAHasMoved

  def _setWhiteRookAMovedFlag(self, *_) -> NoReturn:
    """Single shot setter function for the white rook on file A move flag"""
    self._whiteRookAHasMoved = True

  def _getWhiteRookHMovedFlag(self) -> bool:
    """Single shot getter function for the white rook on file H move flag"""
    return self._whiteRookHHasMoved

  def _setWhiteRookHMovedFlag(self, *_) -> NoReturn:
    """Single shot setter function for the white rook on file H move flag"""
    self._whiteRookHHasMoved = True

  def _getAsMove(self) -> Move:
    """Getter-function for state information as an instance of move"""
    return Move(self._getGrabbedPiece(), self._getGrabbedSquare(),
                self._getHoverPiece(), self._getHoverSquare())

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('General illegal accessor')

  grabbedPiece = property(_getGrabbedPiece, _setGrabbedPiece, _noAcc)
  grabbedSquare = property(_getGrabbedSquare, _setGrabbedSquare, _noAcc)
  grabbedColor = property(_getGrabbedColor, _noAcc, _noAcc)
  hoverSquare = property(_getHoverSquare, _setHoverSquare, _noAcc)
  hoverPiece = property(_getHoverPiece, _setHoverPiece, _noAcc)
  hoverColor = property(_getHoverColor, _noAcc, _noAcc)
  move = property(_getAsMove, _noAcc, _noAcc)
  colorTurn = property(_getTurn, _setTurn, _noAcc)
  hoverTurn = property(_getHoverTurn, _noAcc, _noAcc)
  whiteKingMoved = property(_getWhiteKingMovedFlag, _noAcc, _noAcc)
  blackKingMoved = property(_getBlackKingMovedFlag, _noAcc, _noAcc)
  whiteRookAMoved = property(_getWhiteRookAMovedFlag, _noAcc, _noAcc)
  whiteRookHMoved = property(_getWhiteRookHMovedFlag, _noAcc, _noAcc)
  blackRookAMoved = property(_getBlackRookAMovedFlag, _noAcc, _noAcc)
  blackRookHMoved = property(_getBlackRookHMovedFlag, _noAcc, _noAcc)
  enPassantFile = property(_getEnPassantFile, _setEnPassantFile, _noAcc)
