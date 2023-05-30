"""BaseWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize, QSizeF, Slot
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, \
  QSizePolicy
from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ProceduralError

from visualchess import StaticBoard, CheckboxButton
from workstyle import Label

ic.configureOutput(includeContext=True)

fixedSize = QSizePolicy()
fixedSize.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
fixedSize.setVerticalPolicy(QSizePolicy.Policy.Fixed)

minExpSize = QSizePolicy()
minExpSize.setHorizontalPolicy(QSizePolicy.Policy.MinimumExpanding)
minExpSize.setVerticalPolicy(QSizePolicy.Policy.MinimumExpanding)


class BaseWindow(QMainWindow):
  """BaseWindow
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QMainWindow.__init__(self, parent)
    self._fileMenu = self.menuBar().addMenu('Files')
    self._editMenu = self.menuBar().addMenu('Edit')
    self._helpMenu = self.menuBar().addMenu('Help')
    self._debugMenu = self.menuBar().addMenu('DEBUG')
    self._debugAction01 = self._debugMenu.addAction('Debug 01')
    self.setMouseTracking(True)
    self._baseSize = None
    self._baseWidget = None
    self._baseLayout = None
    self._checkBox = None
    self._mousePos = None
    self._sizeHint = None
    self._board = None

  def debugFunc01(self) -> NoReturn:
    """Debugger"""
    self.repaint()

  def getBoard(self) -> StaticBoard:
    """Getter-function for board"""
    if self._board is None:
      raise ProceduralError('board not ready!')
    if isinstance(self._board, StaticBoard):
      return self._board

  @Slot(QSizeF)
  def sizeToStatusBar(self, size: QSizeF) -> NoReturn:
    """Size slot"""
    msg = """width/height: %.2f | %.2f""" % (size.width(), size.height())
    self.statusBar().showMessage(msg, -1)

  def setupWidgets(self) -> NoReturn:
    """Setting up widgets"""
    self._baseSize = QSize(256, 256)
    self._sizeHint = QSize(256, 256)
    self._checkBox = CheckboxButton()
    self._checkBox.setFixedSize(32, 32)
    self._board = StaticBoard()
    self.setupActions()
    # self._board.setFixedSize(256, 256)

    self._checkBox.clicked.connect(self.lockSizeFunc)
    self.statusBar().addPermanentWidget(self._checkBox)
    self._baseWidget = QWidget()
    self._baseLayout = QHBoxLayout()
    self._baseLayout.addWidget(self._board, )
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)
    self.lockSizeFunc()
    return self.setupActions()

  def setupActions(self) -> NoReturn:
    """Setting up the actions"""
    self.getBoard().boardSize.connect(self.sizeToStatusBar)
    return True

  def show(self) -> NoReturn:
    """Reimplementation of show"""
    if self.setupWidgets():
      QMainWindow.show(self)

  def lockSizeFunc(self, *_) -> NoReturn:
    """Function locking the resizing"""
    if self._checkBox.isChecked():
      self._board.setFixedSize(self._board.contentsRect().size())
      self._board.setSizePolicy(fixedSize)
    else:
      self._board.setSizePolicy(minExpSize)
      # self._board.setMinimumSize(self._baseSize)
      self._board.adjustSize()
