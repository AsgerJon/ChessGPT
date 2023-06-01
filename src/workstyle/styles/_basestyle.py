"""Base style is shared between all style classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QBrush, QPen, QPainter
from worktoy.waitaminute import ProceduralError

from workstyle.styles import Family


class MetaStyle(type):
  """MetaClass used during styling"""

  @classmethod
  def __prepare__(mcls, name: str, __, **_) -> dict:
    """Prepare"""
    return dict(fillColor=QColor(223, 223, 223, 255),
                fillStyle=Qt.BrushStyle.SolidPattern,
                lineColor=QColor(0, 0, 0, 255),
                lineStyle=Qt.PenStyle.SolidLine,
                lineWidth=1,
                fontFamily=Family.courierNew,
                fontSize=16,
                fontWeight=QFont.Weight.Normal,
                fontColor=QColor(0, 0, 0, 255),
                context=None)  # Please note, that context must be present
    # at the class itself.

  def __new__(mcls, name: str, __, nameSpace: dict, **kwargs) -> type:
    """Creates a new style class"""
    out = super().__new__(mcls, name, __, nameSpace)
    context = nameSpace.get('context', None)
    if context is None and not kwargs.get('_base'):
      raise ProceduralError('context', str, None)
    brush = QBrush()
    pen = QPen()
    font = QFont()
    brush.setStyle(nameSpace.get('fillStyle'))
    brush.setColor(nameSpace.get('fillColor'))
    pen.setStyle(nameSpace.get('lineStyle'))
    pen.setColor(nameSpace.get('lineColor'))
    pen.setWidth(nameSpace.get('lineWidth'))
    font.setFamily(nameSpace.get('fontFamily').value)
    font.setPointSize(nameSpace.get('fontSize'))
    font.setWeight(nameSpace.get('fontWeight'))
    setattr(out, 'context', context)
    setattr(out, 'brush', brush)
    setattr(out, 'pen', pen)
    setattr(out, 'font', font)
    setattr(out, 'fontColor', nameSpace.get('fontColor'))
    return out

  def __matmul__(cls, other: QPainter) -> QPainter:
    """Testing style application to QPainter"""
    other.setPen(cls.pen)
    other.setBrush(cls.brush)
    other.setFont(cls.font)
    return other

  def __rshift__(cls, other: dict) -> type:
    name = other.get('name', None)
    if name is None:
      raise ProceduralError('name', str, None)
    return super().__new__(MetaStyle, name, (), other)


class BaseStyle(metaclass=MetaStyle, _base=True):
  """Base style is shared between all style classes
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _styleDictionary = {}

  @classmethod
  def getStyleDictionary(cls) -> dict:
    """Getter-function for style dictionary"""
    return cls._styleDictionary

  @classmethod
  def extendDictionary(cls, ) -> NoReturn:
    """Extends style dictionary"""
    styleDict = BaseStyle.getStyleDictionary()
    styleDict |= {getattr(cls, 'context', None): cls}
    setattr(BaseStyle, '_styleDictionary', styleDict)

  @classmethod
  def __init_subclass__(cls, **kwargs: object) -> object:
    """Records the creation of new subclass"""
    if kwargs.get('_base', False):
      return
    context = getattr(cls, 'context', None)
    if context is None:
      raise ProceduralError('context', str, None)
    cls.extendDictionary()

  @classmethod
  def __subclasscheck__(cls, subclass) -> bool:
    """The Styles are subclasses."""
    return True if BaseStyle in cls.__bases__ else False
