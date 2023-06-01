#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from PySide6.QtCore import QPointF


class BoardDims:
  bezelRatio: float
  boardRatio: float
  gridRatio: float
  bezelPixels: int
  gridPixels: int
  cornerRadiusX: int
  cornerRadiusY: int

  marginLeft: int
  marginTop: int
  marginRight: int
  marginBottom: int

  origin: QPointF
