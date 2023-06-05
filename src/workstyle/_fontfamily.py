"""Family represents font families"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum

from PySide6.QtGui import QFont
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
