"""Square instances represent squares on the chess board"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string
from typing import Any

from PySide6.QtCore import QPointF, QRectF, QSizeF
from worktoy.core import plenty, maybe
from worktoy.parsing import extractArg, maybeTypes
from worktoy.stringtools import stringList

from visualchess import Rank, File


class Square:
  """Square instances represent squares on the chess board
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _NULL = None
  _Instances = []
  __contents__ = {}

  @classmethod
  def rectPoint(cls, rect: QRectF, point: QPointF) -> Square:
    """Locates the square associated with the given rect and point and
    returns it"""
    left, top, = rect.left(), rect.top()
    right, bottom = rect.right(), rect.bottom()
    width, height = rect.width(), rect.height()
    right -= left
    bottom -= top
    x, y = point.x() - left, point.y() - top
    file = File.find(x / width * 8 + 1)
    rank = Rank.find(y / height * 8 + 1)
    return cls(file, rank)

  @classmethod
  def getInstances(cls) -> list[Square]:
    """Getter-function for instances"""
    return cls._Instances

  @classmethod
  def _getNullSquare(cls) -> Square:
    """Getter-function for the null square"""
    if cls._NULL is None:
      cls._NULL = cls(File.NULL, Rank.NULL)
      setattr(cls._NULL, '__null_square__', True)
      return cls._getNullSquare()
    return cls._NULL

  @classmethod
  def validateString(cls, square: str) -> Square:
    """Validates the string and returns it as an instance or returns the
    NULL square."""
    if not isinstance(square, str):
      raise TypeError
    if len(square) - 2:
      return cls._getNullSquare()
    file, rank = [char for char in square]
    if not file.lower() in string.ascii_lowercase[:8]:
      return cls._getNullSquare()
    if not rank.lower() in ['%s' % i for i in range(1, 9)]:
      return cls._getNullSquare()
    return cls(File.find(file), Rank.find(rank))

  def __init__(self, file: File = None, rank: Rank = None) -> None:
    self._file = maybe(file, File.NULL)
    self._rank = maybe(rank, Rank.NULL)

  def getFile(self) -> File:
    """Getter-function for file"""
    if isinstance(self._file, File):
      return self._file

  def getRank(self) -> Rank:
    """Getter-function for rank"""
    if isinstance(self._rank, Rank):
      return self._rank

  def __eq__(self, other: Any) -> bool:
    """Compares to different types"""
    if not self:
      return False
    if isinstance(other, Square):
      if self._file != other._file:
        return False
      if self._rank != other._rank:
        return False
      return True
    if isinstance(other, str):
      return self == self.validateString(other)
    return NotImplemented

  def __bool__(self) -> bool:
    """Only the NULL square is False"""
    if self._file and self._rank:
      return True
    return False

  def getRect(self, boardRect: QRectF) -> QRectF:
    """Getter function for the rectangle that would match this square.
    Please note that the rectangle does not take gridlines into account."""
    if not self:
      return QRectF()
    file, rank = self.getFile(), self.getRank()
    step = boardRect.width() / 2 + boardRect.height() / 2
    size = QSizeF(step, step)
    topLeft = QPointF(file.value * step, rank.value * step)
    return QRectF(topLeft, size)
