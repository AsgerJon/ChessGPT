"""Vector extends the QPointF to vector like function"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPointF
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


class Vector:
  """Vector extends the QPointF to vector like function
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    firstPoint: QPointF
    secondPoint: QPointF
    firstTime: float
    secondTime: float
    firstKeys = stringList('first, start, begin, point0')
    secondKeys = stringList('last, end, point1')
    firstPoint, a, k = extractArg(QPointF, firstKeys, *args, **kwargs)
    secondPoint, a, k = extractArg(QPointF, secondKeys, *a, **k)
    firstTime, a, k = extractArg(float, firstKeys, *a, **k)
    secondTime, a, k = extractArg(float, secondKeys, *a, **k)
    dx = secondPoint.x() - firstPoint.x()
    dy = secondPoint.y() - firstPoint.y()
    dt = secondTime - firstTime
   