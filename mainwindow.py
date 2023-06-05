"""Main window for testing"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize
from icecream import ic
from PySide6.QtWidgets import QMainWindow, QGridLayout

from visualchess import MouseLayout
from workstyle import CoreWidget

ic.configureOutput(includeContext=True)


class MainWindow(QMainWindow):
  """MainWindow
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, ) -> None:
    QMainWindow.__init__(self, )
    self.setMinimumSize(QSize(640, 480))
    self._baseWidget = None
    self._baseLayout = None
    self._board = None
    self._checkButton = None
    self._fileMenu = self.menuBar().addMenu('Files')
    self._editMenu = self.menuBar().addMenu('Edit')
    self._helpMenu = self.menuBar().addMenu('Help')
    self._debugMenu = self.menuBar().addMenu('DEBUG')
    self._saveAction = self._fileMenu.addAction('Save')

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
    self._baseLayout = QGridLayout()  # type: ignore
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

  def _createBoard(self) -> bool:
    """Creator-function for the board"""
    self._board = MouseLayout()
    return False if self._board is None else True

  def getBoard(self) -> MouseLayout:
    """Getter-function for the board widget"""
    if self._board is None:
      self._createBoard()
      return self.getBoard()
    if isinstance(self._board, MouseLayout):
      return self._board
    raise TypeError

  def setupWidgets(self, ) -> bool:
    """Sets up the widgets"""
    self.getBaseLayout().addWidget(self.getBoard(), 0, 0)
    self.getBaseWidget().setLayout(self.getBaseLayout())
    self.setCentralWidget(self.getBaseWidget())
    return self.setupActions()

  def setupActions(self) -> bool:
    """Sets up actions"""
    return True

  def show(self) -> None:
    """Reimplementation ensuring widgets and actions getting setup"""
    if self.setupWidgets():
      QMainWindow.show(self)
