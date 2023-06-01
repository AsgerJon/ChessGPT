"""TimePoints collects QPointF and times"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

import torch
from PySide6.QtCore import QPointF, QObject, QTimer, Qt
from PySide6.QtWidgets import QWidget
from torch import Tensor
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


class TimePoints(QObject):
  """TimePoints collects QPointF and times
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parent: QWidget
    parentKeys = stringList('main, parent')
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    self._parent = parent
    QObject.__init__(self, self._parent)
    self._timer = QTimer()
    self._timer.setTimerType(Qt.TimerType.PreciseTimer)
    self._timer.setParent(self._parent)
    self._timer.setInterval(1000)
    self._timer.setSingleShot(True)
    self._last: QPointF
    self._series: Tensor

  def getLast(self) -> QPointF:
    """Getter-function for last point received"""
    return getattr(self, '_last', None)

  def setLast(self, last: QPointF = None) -> NoReturn:
    """Setter-function for last point received"""
    setattr(self, '_last', last)

  def append(self, point: QPointF, ) -> NoReturn:
    """Appends the given instance of QPointF and epoch to the series. The
    epoch is the time since most recent point."""
    if self.getLast() is None:
      self.setLast(point)
      return self._timer.start()
    if not self._timer.isActive():
      self.setLast()
      return self.append(point)
