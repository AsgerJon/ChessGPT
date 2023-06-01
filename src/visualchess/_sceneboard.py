"""SceneBoard creates a QGraphicsScene for the dynamic user interaction"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QPointF, QSizeF
from PySide6.QtWidgets import QGraphicsScene
from moreworktoy import parentParser


class SceneBoard(QGraphicsScene):
  """SceneBoard creates a QGraphicsScene for the dynamic user interaction
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    QGraphicsScene.__init__(self, parentParser(*args, **kwargs))
    self.setSceneRect(QRectF(QPointF(0, 0), QSizeF(512, 512)))
