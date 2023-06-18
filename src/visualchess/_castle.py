"""Castling enumerates the special castling move"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import NoReturn, Never

from icecream import ic
from worktoy.parsing import extractArg, maybeTypes
from worktoy.stringtools import stringList, monoSpace
from worktoy.waitaminute import ReadOnlyError, UnexpectedStateError

from moreworktoy import Iterify
from visualchess import ChessColor, File, Rank, Square

ic.configureOutput(includeContext=True)


class Castle(Iterify):
  """Castling enumerates the special castling move
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _directionFiles = [[File.E, File.F, File.G], [File.E, File.D, File.C, ]]

  @classmethod
  def _getDirectionFiles(cls, direction: str) -> list[list[File]]:
    """Getter-function for the direction to file dictionary"""
    return cls._directionFiles

  @staticmethod
  def parseDirection(*args, **kwargs) -> str:
    """Parses arguments to find strings defining long or short"""
    directionKeys = stringList('castling, direction')
    direction, args, kwargs = extractArg(str, directionKeys, *args, **kwargs)
    if isinstance(direction, str):
      if direction.replace(' ', '').lower() in stringList('long, short'):
        return direction.replace(' ', '').lower()

  @classmethod
  def createAll(cls, *args, **kwargs) -> NoReturn:
    """Creates the instances"""
    colorNames = stringList('white, black')
    colorRanks = [Rank.rank1, Rank.rank8]
    chessColors = [ChessColor.WHITE, ChessColor.BLACK, ]
    directionNames = stringList('short, long')
    directionFiles = [[File.E, File.F, File.G], [File.E, File.D, File.C, ]]
    for colorName, rank, color in zip(colorNames, colorRanks, chessColors):
      for directionName, files in zip(directionNames, directionFiles):
        squares = [Square.fromFileRank(f, rank) for f in files]
        name = '%s_%s' % (colorName.upper(), directionName.upper())
        instance = cls(color, directionName, name)
        setattr(cls, name, instance)

  @classmethod
  def __old__(cls, *args, **kwargs) -> Castle:
    """Returns an existing instance instead of creating a new one"""
    strArgs = maybeTypes(str, *args)
    colorWord = None
    direction = None
    for word in strArgs:
      if isinstance(word, str):
        if word == 'white':
          colorWord = ChessColor.WHITE
        if word == 'black':
          colorWord = ChessColor.BLACK
        if word in stringList('O-O-O, long, longCastle'):
          direction = 'long'
        if word in stringList('O-O, short, shortCastle'):
          direction = 'short'
    instances = getattr(cls, '__instances__', None)
    if instances is None:
      raise ValueError
    for instance in instances:
      if isinstance(colorWord, str) and isinstance(direction, str):
        if colorWord.lower() in instance.getName().lower():
          if direction in instance.getName().lower():
            return instance

  def __init__(self,
               chessColor: ChessColor,
               direction: str,
               name: str, *args, **kwargs) -> None:
    self._chessColor = chessColor
    self._direction = direction
    self._name = name

  @classmethod
  def fromStr(cls, color: str, direction: str) -> Castle:
    """Returns the instance matching given arguments"""
    for instance in getattr(cls, '__instances__'):
      if instance.direction == direction and instance.color == color:
        return instance
    msg = """Failed to parse arguments: %s and %s!"""
    raise NameError(msg % (color, direction))

  def _getLongFlag(self) -> bool:
    """Getter-function for long flag"""
    files = [square.file for square in self.squares]
    if File.D in files and File.C in files:
      return True
    return False

  def _getShortFlag(self):
    files = [square.file for square in self.squares]
    if File.G in files and File.F in files:
      return True
    return False

  def _getBlackFlag(self) -> bool:
    ranks = [square.rank for square in self.squares]
    return True if Rank.rank8 in ranks else False

  def _getWhiteFlag(self) -> bool:
    ranks = [square.rank for square in self.squares]
    return True if Rank.rank1 in ranks else False

  def _getName(self) -> str:
    """Getter-function for the name of the instance"""
    if isinstance(self._name, str):
      return self._name
    msg = """Expected private variable '_name' to be of type '%s', 
    but received '%s' of type '%s'!"""
    raise TypeError(monoSpace(msg % (str, self._name, type(self._name))))

  def _getSquares(self) -> list[Square]:
    """Getter-function for the list of squares that are required to be
    vacant and not under attack for this move to be allowable."""
    out = []
    for file in self.files:
      out.append(Square.fromFileRank(file, self.rank))
    return out

  def _getFiles(self) -> list[File]:
    """Getter-function for the files"""
    if self.direction == 'short':
      return [File.E, File.F, File.G]
    if self.direction == 'long':
      return [File.E, File.D, File.C]
    raise UnexpectedStateError('Could not recognize direction!')

  def _getRank(self) -> Rank:
    """Getter-function for the rank"""
    if self._chessColor is ChessColor.BLACK:
      return Rank.rank8
    if self._chessColor is ChessColor.WHITE:
      return Rank.rank1
    raise UnexpectedStateError('Could not recognize chess color!')

  def _getColor(self) -> ChessColor:
    """Getter-function for the chess color"""
    if isinstance(self._chessColor, ChessColor):
      return self._chessColor
    msg = """Expected private variable '_chessColor' to be of type '%s', 
    but received '%s' of type '%s'!"""
    raise TypeError(monoSpace(msg % (
      str, self._name, type(self._chessColor))))

  def _getDirection(self) -> str:
    """Getter-function for direction."""
    return 'short' if self.short else 'long'

  def _noAcc(self, *_) -> Never:
    """General Illegal Accessor Function"""
    raise ReadOnlyError('Attempted to access general illegal accessor!')

  name = property(_getName, _noAcc, _noAcc)
  color = property(_getColor, _noAcc, _noAcc)
  rank = property(_getRank, _noAcc, _noAcc)
  files = property(_getFiles, _noAcc)
  squares = property(_getSquares, _noAcc, _noAcc)
  direction = property(_getDirection, _noAcc, _noAcc)
  long = property(_getLongFlag, _noAcc, _noAcc)
  short = property(_getShortFlag, _noAcc, _noAcc)
  black = property(_getBlackFlag, _noAcc, _noAcc)
  white = property(_getWhiteFlag, _noAcc, _noAcc)

  def __bool__(self, ) -> bool:
    """Always returns True"""
    if isinstance(self, Castle):
      return True

  def __hash__(self) -> int:
    """Implementation of hash function"""
    primes = [2, 3, ]
    flags, out = [], 1
    flags.append(1 if self.long else 0)
    flags.append(1 if self.black else 0)
    for p, f in zip(primes, flags):
      out *= (p ** f)
    return out

  def __eq__(self, other: Castle) -> bool:
    """Using hash to determine equality"""
    return False if self.__hash__() - other.__hash__() else True

  def __str__(self) -> str:
    """String Representation"""
    msg = """%s King castles %s"""
    colorName = '%s' % (self.color)
    return msg % (colorName.capitalize(), self.direction)

  def __repr__(self, ) -> str:
    """Code Representation"""
    return 'Castle(\'%s\', \'%s\')' % (self.color, self.direction)
