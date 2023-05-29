"""BaseWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


class BaseWindow(QMainWindow):
  """BaseWindow
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QMainWindow.__init__(self, parent)
    self._baseWidget = None
    self._baseLayout = None
    self._canvas = None

  def setupWidgets(self) -> NoReturn:
    """Setting up widgets"""
    self._baseWidget = QWidget()
    self._baseLayout = QHBoxLayout()
    self._canvas = QWidget()
    self._baseLayout.addWidget(self._canvas, 0, 0, 1, 1, )
    self._baseWidget.setLayout(self._baseWidget)
    self.setCentralWidget(self._baseWidget)

  def show(self) -> NoReturn:
    """Reimplementation of show"""
    self.setupWidgets()
    QMainWindow.show(self)
