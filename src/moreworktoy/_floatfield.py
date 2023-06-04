"""FloatField is a Field representing floating points"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic
from worktoy.core import maybe
from worktoy.field import BaseField

ic.configureOutput(includeContext=True)


class FloatField(BaseField):
  """FloatField is a Field representing floating points
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, name: str, value: float = None) -> None:
    BaseField.__init__(self, name, value)
    self._name = name
    self._value = maybe(value, 0)
    self._type = float
    self._readOnly = False

  def __get__(self, *_) -> float:
    """LOL"""
    out = BaseField.__get__(self, *_)
    if isinstance(out, (int, float)):
      return out
    if isinstance(out, complex):
      return out.real
    raise TypeError

  def __set__(self, _, val: float) -> NoReturn:
    """LOL"""
    return BaseField.__set__(self, self, val, )
