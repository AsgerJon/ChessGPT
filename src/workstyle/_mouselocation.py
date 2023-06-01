"""MouseLocation provides functionalities relating to mouse position"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QObject, Qt, Signal, QPoint, QPointF
from PySide6.QtWidgets import QWidget
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


class MouseLocation(QObject):
  """MouseLocation provides functionalities relating to mouse position
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  cursorMove = Signal(QPointF)

  def __init__(self, *args, **kwargs) -> None:
    parent: QWidget
    parentKeys = stringList('main, parent')
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    self._parent = parent
    QObject.__init__(self, self._parent)
    self._point = None

  def setPoint(self, point: QPointF) -> NoReturn:
    """Setter-function for cursor position"""
    