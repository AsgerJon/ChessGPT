"""BezelStyle defines the style applied to the boundary surrounding the
chessboard"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from workstyle.styles import BaseStyle


class BezelStyle(BaseStyle):
  """BezelStyle defines the style applied to the boundary surrounding the
  chessboard # #8A0904
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  context = 'bezels'
  fillColor = QColor(8 * 16, 9, 4, 255)
  lineStyle = Qt.PenStyle.NoPen
