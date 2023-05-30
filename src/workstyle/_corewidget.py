"""CoreWidget subclasses QWidget providing common and general
functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn

from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


class CoreWidget(QWidget):
  """CoreWidget subclasses QWidget providing common and general
  functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QWidget.__init__(self, )
    self.setMouseTracking(True)

  @abstractmethod
  def setupWidgets(self) -> NoReturn:
    """Sets up the widgets"""

  @abstractmethod
  def setupActions(self) -> NoReturn:
    """Sets up the actions"""

  def show(self) -> NoReturn:
    """Runs the setupWidgets and setupActions methods before apply the
    QWidget show."""
    self.setupWidgets()
    self.setupActions()
    QWidget.show(self)
