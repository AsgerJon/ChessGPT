"""Main window for testing"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QKeyEvent
from icecream import ic
from PySide6.QtWidgets import QMainWindow, QGridLayout

from workstyle import CoreWidget, Indicator
from visualchess import PieceGrabbing as OMGWIDGET
from visualchess import Sound

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
    self._indicator = None
    self._fileMenu = self.menuBar().addMenu('Files')
    self._editMenu = self.menuBar().addMenu('Edit')
    self._helpMenu = self.menuBar().addMenu('Help')
    self._debugMenu = self.menuBar().addMenu('DEBUG')
    self._debugAction01 = self._debugMenu.addAction('Debug01', )
    self._debugAction02 = self._debugMenu.addAction('Debug02', )
    self._debugAction03 = self._debugMenu.addAction('Debug03', )
    self._debugAction04 = self._debugMenu.addAction('Debug04', )
    self._debugAction01.triggered.connect(self._debugFunc01)
    self._debugAction02.triggered.connect(self._debugFunc02)
    self._debugAction03.triggered.connect(self._debugFunc03)
    self._debugAction03.triggered.connect(self._debugFunc04)
    self._saveAction = self._fileMenu.addAction('Save')

  def _createIndicator(self) -> NoReturn:
    """Creator function for Indicator widget"""
    self._indicator = Indicator()

  def getIndicator(self) -> Indicator:
    """Getter-function for the indicator widget"""
    if self._indicator is None:
      self._createIndicator()
      return self.getIndicator()
    if isinstance(self._indicator, Indicator):
      return self._indicator
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
    self._board = OMGWIDGET()
    return False if self._board is None else True

  def getBoard(self) -> OMGWIDGET:
    """Getter-function for the board widget"""
    if self._board is None:
      self._createBoard()
      return self.getBoard()
    if isinstance(self._board, OMGWIDGET):
      return self._board
    raise TypeError

  def setupWidgets(self, ) -> bool:
    """Sets up the widgets"""
    self.getBaseLayout().addWidget(self.getBoard(), 0, 0)
    self.getBaseLayout().addWidget(self.getIndicator(), 1, 0)
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

  def _debugFunc01(self) -> NoReturn:
    """Debugger 1"""
    Sound.slide.play()

  def _debugFunc02(self) -> NoReturn:
    """Debugger 2"""

  def _debugFunc03(self) -> NoReturn:
    """Debugger 3"""

  def _debugFunc04(self) -> NoReturn:
    """Debugger 4"""
