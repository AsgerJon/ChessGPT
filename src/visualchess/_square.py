"""Square is a simple dataclass representing each of the squares on the
chess board"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Never, Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QColor
from worktoy import maybe, searchKeys, maybeTypes

from visualchess import showPiece


class Piece:
  """Piece is a simpledata class representing each chess piece
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _empty = None

  @classmethod
  def emptyPiece(cls) -> Piece:
    """Getter-function for the empty piece. This 'piece' is present on empty
    squares"""
    if cls._empty is None:
      cls._empty = cls()
      cls._empty._name = '__empty__'
      return cls.emptyPiece()
    return cls._empty

  def __init__(self, *args, **kwargs) -> None:
    self._name = None
    self._color = None
    self._currentSquare = None
    self._pix = None

  def _leftEnPassant(self) -> bool:
    """Flag indicating if en passant to the left is available"""
    raise NotImplementedError

  def __bool__(self) -> bool:
    """All pieces are Truthy except for the empty piece"""
    return False if self._name == '__empty__' else True

  def _getCurrentSquare(self) -> Square:
    """Getter-function for the current square"""
    return self._currentSquare

  def _setCurrentSquare(self, square: Square) -> NoReturn:
    """Setter-function for the current square"""
    self._currentSquare = square

  def _delCurrentSquare(self, ) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read Only')

  def reachableSquares(self) -> list[Square]:
    """List of reachable squares"""
    raise NotImplementedError('Not implemented yet!')

  def _getColor(self) -> Optional[str]:
    """Getter-function for the color of this piece"""
    if self:
      return self._color
    return None

  def _setColor(self, color: str) -> NoReturn:
    """Getter-function for the color of this piece"""
    self._color = color

  def _delColor(self, ) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read Only')

  def _getName(self) -> str:
    """Getter-function for name """
    return self._name

  def _setName(self, name: str) -> NoReturn:
    """Getter-function for name """
    self._name = name

  def _delName(self, ) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read Only')

  def _createPixCache(self) -> NoReturn:
    """Creator-function for cached pixmap"""
    self._pix = showPiece(self.name, self.color)

  def _getPixCache(self) -> QPixmap:
    """Getter-function for cached pixmap"""
    if not self:
      pix = QPixmap(QSize(32, 32))
      pix.fill(QColor(0, 0, 0, 0, ))
      return pix
    if self._pix is None:
      self._createPixCache()
      return self._getPixCache()
    return self._pix

  def _setPixCache(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error!')

  def _delPixCache(self) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read Only Error!')

  square = property(_getCurrentSquare, _setCurrentSquare, _delCurrentSquare)
  color = property(_getColor, _setColor, _delColor)
  name = property(_getName, _setName, _delName)
  pix = property(_getPixCache, _setPixCache, _delPixCache)


class Square:
  """Square is a simple dataclass representing each of the squares on the
  chess board.
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _noneSquare = None

  @classmethod
  def _getNoneSquare(cls) -> Square:
    """Getter-function for the none square. This special instance
    represents squares not in the game. A captured piece should be on this
    square. Multiple pieces can be on this square. This is because this
    square is not equal to itself."""
    if cls._noneSquare is None:
      cls._noneSquare = cls()
      cls._noneSquare._file = ''
      cls._noneSquare._rank = ''
      return cls._getNoneSquare()
    return cls._noneSquare

  def __init__(self, *args, **kwargs) -> None:
    strArgs = maybeTypes(str, *args)
    chars = [arg for arg in strArgs if len(arg) == 1]
    fileKwarg = searchKeys('file', 'x') @ str >> kwargs
    rankKwarg = searchKeys('rank', 'y') @ str >> kwargs
    fileArg = [char.upper() for char in chars if char.lower() in 'abcdefgh']
    rankArg = [char.upper() for char in chars if char.lower() in '12345678']
    file = maybe(fileKwarg, fileArg, None)
    rank = maybe(rankKwarg, rankArg, None)
    if file is None or rank is None:
      raise ValueError('Unable to parse square!')
    self._file = file
    self._rank = rank
    self._piece = None

  def _getPiece(self) -> Piece:
    """Getter-function for the current piece"""
    return maybe(self._piece, Piece.emptyPiece())

  def _setPiece(self, piece: Piece) -> NoReturn:
    """Getter-function for the current piece"""
    self._piece = piece

  def _delPiece(self, ) -> Never:
    """Illegal deleter function"""
    raise TypeError('read only variable!')

  piece = property(_getPiece, _setPiece, _delPiece)
