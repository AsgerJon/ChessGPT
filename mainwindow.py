"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout

from visualchess import TestWidget, StaticBoard, CheckButton
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
    self._checkButton = None

  def setupWidgets(self) -> bool:
    """Sets up the widgets"""
    self._baseWidget = CoreWidget()
    self._baseLayout = QGridLayout()
    self._staticBoard = StaticBoard()
    self._checkButton = CheckButton()
    self._checkButton.setFixedSize(QSize(48, 48))
    self._baseLayout.addWidget(self._staticBoard, 0, 0)
    self._baseLayout.addWidget(self._checkButton, 1, 1)
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)
    return self.setupActions()

  def setupActions(self) -> bool:
    """Sets up the widgets"""
    self._checkButton.clicked.connect(self._handleCheckBoxClick)
    return True

  def _handleCheckBoxClick(self) -> NoReturn:
    """Handler function for checkbox click"""
    if self._checkButton.isChecked():
      return self._staticBoard.lockSize()
    return self._staticBoard.unlockSize()

  def show(self) -> NoReturn:
    """Reimplementation ensuring widgets and actions getting setup"""
    if self.setupWidgets():
      QMainWindow.show(self)
