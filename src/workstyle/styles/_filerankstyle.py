"""FileRankStyle defines the style of the letters and numbers indicate
files and ranks respectively"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from workstyle.styles import Family, BaseStyle


class FileRankStyle(BaseStyle):
  context = 'fileRankStyle'
  fontFamily = Family.sourceCodePro
  fontSize = 12
  lineColor = QColor(191, 191, 255, 255)
  lineStyle = Qt.PenStyle.SolidLine
  lineWidth = 1
