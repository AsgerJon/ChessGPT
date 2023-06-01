#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from typing import NoReturn

from PySide6.QtGui import QPainter
from workstyle.styles import Family as Family


class MetaStyle(type):
  @classmethod
  def __prepare__(mcls, name: str, __, **_) -> dict: ...

  def __new__(mcls, name: str, __, nameSpace: dict, **kwargs) -> type: ...

  def __matmul__(cls, other: QPainter) -> QPainter: ...

  def __rshift__(cls, other: dict) -> type: ...


class BaseStyle(metaclass=MetaStyle):
  _styleDictionary: dict

  @classmethod
  def getStyleDictionary(cls) -> dict: ...

  @classmethod
  def extendDictionary(cls, ) -> NoReturn: ...

  @classmethod
  def __init_subclass__(cls, **kwargs: object) -> object: ...

  @classmethod
  def __subclasscheck__(cls, subclass) -> bool: ...
