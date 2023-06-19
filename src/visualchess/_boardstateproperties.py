"""_BoardStateProperties provides properties to the BoardState class"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Never

from icecream import ic
from worktoy.waitaminute import ReadOnlyError

from visualchess import ChessColor, ChessPiece, Square

ic.configureOutput(includeContext=True)


class _BoardStateProperties:
  """_BoardStateProperties provides properties to the BoardState class
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *__, **_) -> None:
    self._contents = {s: ChessPiece.EMPTY for s in Square}
    self._activeColor = ChessColor.WHITE
    self._grabbedPiece = ChessPiece.EMPTY
    self._grabbedSquare = Square.NULL
    self._hoverPiece = ChessPiece.EMPTY
    self._hoverSquare = Square.NULL

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

  def getGrabbedPiece(self) -> ChessPiece:
    """Getter-function for the piece currently grabbed"""
    return self._grabbedPiece

  def setGrabbedPiece(self, chessPiece: ChessPiece) -> NoReturn:
    """Getter-function for the piece currently grabbed"""
    self._grabbedPiece = chessPiece

  def delGrabbedPiece(self) -> NoReturn:
    """Deleter-function for the piece currently grabbed"""

  def getGrabbedSquare(self) -> Square:
    """Getter-function for square of the currently grabbed square"""
    return self._grabbedSquare

  def setGrabbedSquare(self, square: Square) -> NoReturn:
    """Setter-function for square of the currently grabbed square"""
    self._grabbedSquare = square

  def delGrabbedSquare(self, ) -> NoReturn:
    """Deleter-function for square of the currently grabbed square"""

  def getHoverSquare(self) -> Square:
    """Getter-function for hover square"""
    return self._hoverSquare

  def setHoverSquare(self, square: Square) -> NoReturn:
    """Setter-function for hover square"""
    self._hoverSquare = square

  def delHoverSquare(self, ) -> NoReturn:
    """Deleter-function for hover square"""
    self._hoverSquare = Square.NULL

  def getHoverPiece(self) -> ChessPiece:
    """Getter-function for hovered piece"""
    return self._hoverPiece

  def setHoverPiece(self, chessPiece: ChessPiece) -> NoReturn:
    """Setter-function for hovered piece"""
    self._hoverPiece = chessPiece

  def delHoverPiece(self) -> NoReturn:
    """Deleter-function for hovered piece"""
    self._hoverPiece = ChessPiece.EMPTY

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('lowerName')

  grabbedPiece = property(getGrabbedPiece, setGrabbedPiece, delGrabbedPiece)
  grabbedSquare = property(getGrabbedSquare,
                           setGrabbedSquare,
                           delGrabbedSquare)
  hoverPiece = property(getHoverPiece, setHoverPiece, delHoverPiece)
  hoverSquare = property(getHoverSquare, setHoverSquare, delHoverSquare)
