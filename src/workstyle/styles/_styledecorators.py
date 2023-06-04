"""This module provides the style decorators"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen, QFont
from worktoy.core import maybe
from worktoy.field import BaseField
from worktoy.parsing import maybeType


class Family(Enum):
  """Enum specifying font families"""
  arial = "Arial"
  timesNewRoman = "Times New Roman"
  courierNew = "Courier New"
  verdana = "Verdana"
  cambria = "Cambria"
  tahoma = "Tahoma"
  calibri = "Calibri"
  comicSansMs = "Comic Sans MS"
  helvetica = "Helvetica"
  geneva = "Geneva"
  lucidaGrande = "Lucida Grande"
  dejavuSans = "DejaVu Sans"
  dejavuSerif = "DejaVu Serif"
  dejavuSansMono = "DejaVu Sans Mono"
  liberationSans = "Liberation Sans"
  liberationSerif = "Liberation Serif"
  liberationMono = "Liberation Mono"
  ubuntu = "Ubuntu"
  cantarell = "Cantarell"
  droidSans = "Droid Sans"
  droidSerif = "Droid Serif"
  roboto = "Roboto"
  robotoCondensed = "Roboto Condensed"
  robotoMono = "Roboto Mono"
  notoSans = "Noto Sans"
  notoSerif = "Noto Serif"
  notoSansMono = "Noto Sans Mono"
  sourceSansPro = "Source Sans Pro"
  sourceSerifPro = "Source Serif Pro"
  sourceCodePro = "Source Code Pro"
  modern = "Modern No. 20"

  def asQFont(self, size: int = None) -> QFont:
    """Creates a QFont version of self at font size given"""
    font = QFont()
    font.setFamily(self.value)
    font.setPointSize(maybe(size, 12))
    return font


class BrushField(BaseField):
  """Decorating class with a QBrush field
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, ) -> None:
    self._owner = None
    self._instance = None
    self._name = maybeType(str, *args)
    self._color = maybeType(QColor, *args)
    self._type = QBrush
    self._value = QBrush()
    self._value.setStyle(Qt.BrushStyle.SolidPattern)
    self._value.setColor(self._color)
    self._defVal = self._value
    self._readOnly = True
    BaseField.__init__(self, self._name, self._value, readOnly=True, )


class PenField(BaseField):
  """Decorating class with a QPen field
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, ) -> None:
    self._owner = None
    self._instance = None
    self._name = maybeType(str, *args)
    self._color = maybeType(QColor, *args)
    self._width = maybeType(int, *args)
    self._type = QPen
    self._value = QPen()
    self._value.setStyle(Qt.PenStyle.SolidLine)
    self._value.setColor(self._color)
    self._value.setWidth(self._width)
    self._defVal = self._value
    self._readOnly = True
    BaseField.__init__(self, self._name, self._value, readOnly=True, )


class FontField(BaseField):
  """Decorating class with QFont field
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, ) -> None:
    self._owner = None
    self._instance = None
    self._name = maybeType(str, *args)
    self._family = maybeType(Family, *args)
    self._size = maybeType(int, *args)
    self._type = QFont
    self._value = QFont()
    self._value.setFamily(self._family)
    self._value.setPointSize(self._size)
    self._defVal = self._value
    self._readOnly = True
    BaseField.__init__(self, self._name, self._value, readOnly=True, )
