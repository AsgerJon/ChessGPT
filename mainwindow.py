"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QGridLayout

from visualchess import CheckButton, SquarePaint
from workstyle import CoreWidget


class MainWindow(QMainWindow):
  """MainWindow
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, ) -> None:
    QMainWindow.__init__(self, )
    self._baseWidget = None
    self._baseLayout = None
    self._board = None
    self._checkButton = None

  def _createCheckButton(self) -> bool:
    """Creator-function for check button"""
    self._checkButton = CheckButton()
    return False if self._checkButton is None else True

  def getCheckButton(self) -> CheckButton:
    """Getter-function for check button"""
    if self._checkButton is None:
      self._createCheckButton()
      return self.getCheckButton()
    if isinstance(self._checkButton, CheckButton):
      return self._checkButton
    raise TypeError

  def _createBoard(self) -> bool:
    """Creator-function for the board"""
    self._board = SquarePaint()
    return False if self._board is None else True

  def getBoard(self) -> SquarePaint:
    """Getter-function for the board widget"""
    if self._board is None:
      self._createBoard()
      return self.getBoard()
    if isinstance(self._board, SquarePaint):
      return self._board
    raise TypeError

  def _createBaseWidget(self) -> bool:
    """Creator-function for the base widget"""
    self._baseWidget = CoreWidget()
    return False if self._baseWidget is None else True

  def getBaseWidget(self) -> CoreWidget:
    """Getter-function for base widget"""
    if self._baseWidget is None:
      if self._createBaseWidget():
        return self.getBaseWidget()
      raise TypeError
    if isinstance(self._baseWidget, CoreWidget):
      return self._baseWidget
    raise TypeError

  def _createBaseLayout(self) -> bool:
    """Creator-function for the base layout"""
    self._baseLayout = QGridLayout()
    return False if self._baseLayout is None else True

  def getBaseLayout(self) -> QGridLayout:
    """Getter-function for base layout"""
    if self._baseLayout is None:
      if self._createBaseLayout():
        return self.getBaseLayout()
      raise TypeError
    if isinstance(self._baseLayout, QGridLayout):
      return self._baseLayout
    raise TypeError

  def setupWidgets(self) -> bool:
    """Sets up the widgets"""
    self.getCheckButton().setFixedSize(QSize(48, 48))
    self.getBaseLayout().addWidget(self.getCheckButton(), 1, 1)
    self.getBaseWidget().setLayout(self.getBaseLayout())
    self.setCentralWidget(self.getBaseWidget())
    return self.setupActions()

  def setupActions(self) -> bool:
    """Sets up the widgets"""
    self.getCheckButton().clicked.connect(self._handleCheckBoxClick)
    return True

  def _handleCheckBoxClick(self) -> bool:
    """Handler function for checkbox click"""
    if self.getCheckButton().isChecked():
      self.getBoard().lockSize()
    if not self.getCheckButton().isChecked():
      self.getBoard().unlockSize()
    return True if self.getCheckButton().isChecked() else False

  def show(self) -> None:
    """Reimplementation ensuring widgets and actions getting setup"""
    if self.setupWidgets():
      QMainWindow.show(self)
