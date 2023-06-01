"""This file specifies geometric information about the static chessboard
such as relative bezels and gridlines"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPointF


class BoardDims:
  """Board dimensions"""
  bezelRatio = 32 / 400
  boardRatio = 1 - bezelRatio
  gridRatio = 8 / 400

  bezelPixels = 32
  marginLeft = 16
  marginTop = 16
  marginRight = 16
  marginBottom = 16
  gridPixels = 3
  cornerRadiusX = 8
  cornerRadiusY = 8

  origin = QPointF(0, 0)
