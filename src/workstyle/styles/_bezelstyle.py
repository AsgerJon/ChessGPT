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
  chessboard
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  context = 'bezels'
  fillColor = QColor(127, 127, 239, 255)
  lineStyle = Qt.PenStyle.NoPen
