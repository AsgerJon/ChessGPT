"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize, QRect, QPoint
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import QMainWindow, QGridLayout

from visualchess import CheckButton, SquarePaint
from workstyle import CoreWidget
from workstyle.styles import FileData


class MainWindow(QMainWindow):
  """MainWindow
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def getDefaultPixName() -> str:
    """Getter-function for default save file name"""
    return FileData.getImageFilePath()

  @staticmethod
  def paintPixmap() -> QPixmap:
    """Creates a pixmap of the chessboard"""
    pix = FileData.createPixmap()
    SquarePaint.paintEvent(pix, QRect(QPoint(0, 0), pix.size()))
    return pix

  @staticmethod
  def savePixmapFunc() -> NoReturn:
    """Saves the pixmap showing the board to the disk"""
    pix = MainWindow.paintPixmap()
    fid = MainWindow.getDefaultPixName()
    fmt = FileData.imageFormat
    pix.save(fid, fmt)

  def __init__(self, ) -> None:
    QMainWindow.__init__(self, )
    self._baseWidget = None
    self._baseLayout = None
    self._board = None
    self._checkButton = None
    self._fileMenu = self.menuBar().addMenu('Files')
    self._editMenu = self.menuBar().addMenu('Edit')
    self._helpMenu = self.menuBar().addMenu('Help')
    self._debugMenu = self.menuBar().addMenu('DEBUG')
    self._saveAction = self._fileMenu.addAction('Save')
    self._saveAction.triggered.connect(self.savePixmapFunc)

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

  def setupWidgets(self) -> bool:
    """Sets up the widgets"""
    self.getCheckButton().setFixedSize(QSize(48, 48))
    self.getBaseLayout().addWidget(self.getBoard(), 0, 0)
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

  def resizeEvent(self, event: QResizeEvent) -> NoReturn:
    """Resize event implementation"""
    self.getBoard().repaint()
