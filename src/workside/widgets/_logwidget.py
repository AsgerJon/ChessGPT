"""LogWidget is as development widget. Instead of print statement for
debugging, call the 'tellMe' method on this widget."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QFileDialog, QLabel
from icecream import ic

from workside.widgets import CoreWidget
from workside.widgets import ListWidget
from workside.styles import Family

ic.configureOutput(includeContext=True)


class LogWidget(CoreWidget):
  """LogWidget is as development widget. Instead of print statement for
  debugging, call the 'tellMe' method on this widget.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  hoveredLog = Signal(str)
  clickedLog = Signal(str)
  doubleClickedLog = Signal(str)

  overWritingSaveFile = Signal(str)
  receivedLog = Signal(str)

  def __init__(self, *args, **kwargs) -> None:
    self._baseLayout = None
    self._listWidget = None
    self._fileName = None
    self._headerFont = None
    self._headerLabel = None
    self._saveFileDialog = None
    CoreWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    # self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
    #                    QSizePolicy.Policy.MinimumExpanding, )

  def setupWidgets(self) -> NoReturn:
    """Sets up the widgets"""
    self._baseLayout = QGridLayout()
    self._baseLayout.addWidget(self._getListWidget(), 1, 0)
    self._baseLayout.addWidget(self._getHeaderLabel(), 0, 0)
    self.setLayout(self._baseLayout)

  def setupActions(self) -> NoReturn:
    """Sets up the actions"""
    self._getListWidget().itemEntered.connect(
      self.hoveredLog.emit)
    self._getListWidget().itemClicked.connect(
      self.clickedLog.emit)
    self._getListWidget().itemDoubleClicked.connect(
      self.doubleClickedLog.emit)

  @Slot()
  def initiateSaveLogs(self) -> NoReturn:
    """Saves the logs opening a save file dialog if necessary."""
    fileName = self._getFileName()
    if not isinstance(fileName, str):
      raise TypeError
    if not os.path.exists(fileName):
      self.overWritingSaveFile.emit()
    dirName = os.path.basename(fileName)
    if not os.path.exists(dirName):
      raise NotADirectoryError
    return self.saveLogs(fileName)

  @Slot()
  def saveLogs(self, ) -> NoReturn:
    """Performs the saving operation on the fileName received."""
    self._getListWidget().saveContents(self._getFileName())

  def _createFont(self) -> NoReturn:
    """Creator-function for the header font"""
    self._headerFont = QFont()
    self._headerFont @ Family.modern
    self._headerFont.setPointSize(24)

  def _getFont(self) -> QFont:
    """Getter-function for the font"""
    if self._headerFont is None:
      self._createFont()
      return self._getFont()
    if isinstance(self._headerFont, QFont):
      return self._headerFont
    raise TypeError

  def _createHeaderLabel(self) -> NoReturn:
    """Creator-function for the header label"""
    self._headerLabel = QLabel()
    self._headerLabel.setText('Logged Events')
    self._headerLabel.setFont(self._getFont())

  def _getHeaderLabel(self, ) -> QLabel:
    """Getter-function for the header label"""
    if self._headerLabel is None:
      self._createHeaderLabel()
      return self._getHeaderLabel()
    if isinstance(self._headerLabel, QLabel):
      return self._headerLabel
    raise TypeError

  def _createListWidget(self) -> NoReturn:
    """Creator-function for the list widget"""
    self._listWidget = ListWidget()
    # self._listWidget.itemEntered.connect(self.handleHovered)

  def _getListWidget(self) -> ListWidget:
    """Returns the list widget"""
    if self._listWidget is None:
      self._createListWidget()
      return self._getListWidget()
    if isinstance(self._listWidget, ListWidget):
      return self._listWidget

  def _createBaseLayout(self) -> NoReturn:
    """Creator-function for the base layout"""
    self._baseLayout = QGridLayout()

  def _getBaseLayout(self) -> QGridLayout:
    """Returns the base layout"""
    if self._baseLayout is None:
      self._createBaseLayout()
      return self._getBaseLayout()
    if isinstance(self._baseLayout, QGridLayout):
      return self._baseLayout

  def _createSaveFileDialog(self) -> NoReturn:
    """Creator-function for the save file dialog"""
    self._saveFileDialog = QFileDialog()
    self._saveFileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
    self._saveFileDialog.setViewMode(QFileDialog.ViewMode.Detail)
    self._saveFileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    self._saveFileDialog.fileSelected.connect(self._setFileName)

  def _getSaveFileDialog(self) -> QFileDialog:
    """Getter-function for the save file dialog"""
    if self._saveFileDialog is None:
      self._createSaveFileDialog()
      return self._getSaveFileDialog()
    if isinstance(self._saveFileDialog, QFileDialog):
      return self._saveFileDialog
    raise TypeError

  def _setFileName(self, fileName: str = None) -> bool:
    """Setter-function for the file name"""
    if isinstance(fileName, str):
      dirName = os.path.abspath(fileName)
      if os.path.exists(dirName):
        self._fileName = fileName
        return True
      else:
        os.makedirs(dirName, exist_ok=True)
        return self._setFileName(fileName)
    return False

  def _getFileName(self, **kwargs) -> str:
    """Getter-function for file name"""
    if self._fileName is None:
      _recursion = kwargs.get('recursion', 0)
      self._getSaveFileDialog().show()
      if _recursion > 3:
        raise RecursionError()
      return self._getFileName(_recursion=_recursion + 1)
    if isinstance(self._fileName, str):
      return self._fileName
    raise TypeError

  def tellMe(self, msg: str) -> NoReturn:
    """Logs the message received"""
    self._getListWidget().insertText(msg)
    self.update()
