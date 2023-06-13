"""Family represents font families"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from enum import Enum

from PySide6.QtGui import QFont, QPainter
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.core import maybe

ic.configureOutput(includeContext=True)


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

  def __rmatmul__(self, other: QObject) -> QObject | QPainter:
    """Applies font family to other"""
    if isinstance(other, QFont):
      other.setFamily(self.value)
      return other
    if isinstance(other, QWidget) or isinstance(other, QPainter):
      font = other.font()
      font.setFamily(self.value)
      other.setFont(font)
      if isinstance(other, QWidget) or isinstance(other, QPainter):
        return other
      raise TypeError
    return NotImplemented
