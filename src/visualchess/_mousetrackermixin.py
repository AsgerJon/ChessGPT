"""MouseTrackerMixin emits a signal indicating the cursor position"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QMouseEvent


class MouseTrackerMixin:
  """MouseTrackerMixin emits a signal indicating the cursor position
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  mousePosition = Signal(QPoint)

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation"""
    self.mousePosition.emit(event.pos())
