"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtWidgets import QMainWindow, QVBoxLayout

from visualchess import TestWidget, StaticBoard
from workstyle import CoreWidget


class MainWindow(QMainWindow):
  """MainWindow
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, ) -> None:
    QMainWindow.__init__(self, )
    self._baseWidget = None
    self._baseLayout = None
    self._staticBoard = None

  def setupWidgets(self) -> bool:
    """Sets up the widgets"""
    self._baseWidget = CoreWidget()
    self._baseLayout = QVBoxLayout()
    self._staticBoard = StaticBoard()
    self._baseLayout.addWidget(self._staticBoard)
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)
    return self.setupActions()

  def setupActions(self) -> bool:
    """Sets up the widgets"""
    return True

  def show(self) -> NoReturn:
    """Reimplementation ensuring widgets and actions getting setup"""
    if self.setupWidgets():
      QMainWindow.show(self)
