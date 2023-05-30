"""CoreWidget subclasses QWidget providing common and general
functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn

from PySide6.QtWidgets import QWidget
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


class CoreWidget(QWidget):
  """CoreWidget subclasses QWidget providing common and general
  functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def parseParent(*args, **kwargs) -> QWidget:
    """Parses arguments to parent"""
    parentKeys = stringList('parent, main, mainWindow, window')
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    if isinstance(parent, QWidget):
      return parent

  def __init__(self, *args, **kwargs) -> None:
    parent = self.parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    self.setupWidgets()
    self.setupActions()

  def setupWidgets(self) -> NoReturn:
    """Sets up the widgets"""

  def setupActions(self) -> NoReturn:
    """Sets up the actions"""
