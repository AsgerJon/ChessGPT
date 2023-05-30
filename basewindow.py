"""BaseWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QSizePolicy
from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from visualchess import StaticBoard, CheckboxButton
from workstyle import Button

fixedSize = QSizePolicy()
fixedSize.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
fixedSize.setVerticalPolicy(QSizePolicy.Policy.Fixed)

minExpSize = QSizePolicy()
minExpSize.setHorizontalPolicy(QSizePolicy.Policy.MinimumExpanding)
minExpSize.setVerticalPolicy(QSizePolicy.Policy.MinimumExpanding)

ic.configureOutput(includeContext=True)


class BaseWindow(QMainWindow):
  """BaseWindow
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QMainWindow.__init__(self, parent)
    self._baseSize = None
    self._baseWidget = None
    self._baseLayout = None
    self._canvas = None
    self._checkBox = None
    self._mousePos = None
    self._sizeHint = None

  def setupWidgets(self) -> NoReturn:
    """Setting up widgets"""
    self._baseSize = QSize(256, 256)
    self._sizeHint = QSize(256, 256)
    self._checkBox = CheckboxButton()
    self._checkBox.setFixedSize(32, 32)

    self._checkBox.clicked.connect(self.lockSizeFunc)
    # self.statusBar().addPermanentWidget(self._mouseTrack)
    self.statusBar().addPermanentWidget(self._checkBox)
    self._baseWidget = QWidget()
    self._baseLayout = QHBoxLayout()
    self._canvas = StaticBoard()
    self._baseLayout.addWidget(self._canvas, )
    self._baseWidget.setLayout(self._baseLayout)
    self.setCentralWidget(self._baseWidget)

  def show(self) -> NoReturn:
    """Reimplementation of show"""
    self.setupWidgets()
    QMainWindow.show(self)

  def lockSizeFunc(self, *_) -> NoReturn:
    """Function locking the resizing"""
    if self._checkBox.isChecked():
      self._canvas.setFixedSize(self._canvas.contentsRect().size())
      self._canvas.setSizePolicy(fixedSize)
    else:
      self._canvas.setSizePolicy(minExpSize)
      self._canvas.setMinimumSize(self._baseSize)

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation"""
    ic(event.buttons())
    ic(Qt.MouseButton.LeftButton == event.buttons())
