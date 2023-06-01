#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainter
from _typeshed import Incomplete
from enum import Enum
from moreworktoy import InstanceIteration
from typing import NoReturn, Optional
from worktoy.typetools import TypeBag as TypeBag


class File(Enum):
  A: int
  B: int
  C: int
  D: int
  E: int
  F: int
  G: int
  H: int

  @classmethod
  def find(cls, index: int | str) -> File: ...

  @classmethod
  def byValue(cls, val: int) -> File: ...

  def __matmul__(self, other: Rank) -> Shade: ...

  @classmethod
  def _getFromStr(cls, index) -> File:
    pass

  @classmethod
  def _getFromInt(cls, index) -> File:
    pass


class Rank(Enum):
  rank0: int
  rank1: int
  rank2: int
  rank3: int
  rank4: int
  rank5: int
  rank6: int
  rank7: int

  @classmethod
  def find(cls, index: int | str) -> Rank: ...

  @classmethod
  def byValue(cls, val: int) -> Rank: ...

  def __matmul__(self, other: File) -> Shade: ...

  @classmethod
  def _getFromInt(cls, index) -> Rank:
    pass

  @classmethod
  def _getFromStr(cls, index) -> Rank:
    pass


class Shade(Enum):
  DARK: int
  LIGHT: int

  def __bool__(self) -> bool: ...

  def __eq__(self, other: Shade) -> bool: ...

  def getStyle(self) -> None: ...


class Square(InstanceIteration):
  _instances = None
  __index__: Incomplete

  @classmethod
  def getNull(cls) -> Square: ...

  @classmethod
  def createAll(cls) -> NoReturn: ...

  @classmethod
  def pointRect(cls, point: QPointF, boardRect: QRectF) -> Optional[
    Square]: ...

  @classmethod
  def __new__(cls, *args, **kwargs) -> Square: ...

  def __init__(self, *args, **kwargs) -> None: ...

  def getFile(self) -> File: ...

  def getRank(self) -> Rank: ...

  def getShade(self) -> Shade: ...

  def rectOnBoard(self, boardRect: QRectF) -> QRectF: ...

  def applyPaint(self, painter: QPainter) -> NoReturn: ...
