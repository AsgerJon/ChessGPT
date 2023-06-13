"""ListWidget subclasses QListWidget creating a list of items in a
scrollable area."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import time
from typing import NoReturn

from PySide6.QtCore import Slot
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QGridLayout
from icecream import ic
from worktoy.core import maybe

from workside.widgets import CoreWidget

ic.configureOutput(includeContext=True)


class ListWidget(QListWidget):
  """ListWidget subclasses QListWidget creating a list of items in a
  scrollable area.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    parent = CoreWidget.parseParent(*args, **kwargs)
    QListWidget.__init__(self, parent)
    self.setMouseTracking(True)
    self._logs = []
    self._baseLayout = None
    self._saveFileDialog = None
    self._loadFileDialog = None
    self._name = None
    self._hoverItem = None
    self._clickedItem = None
    self._doubleClicked = None

  def _getHoverItem(self) -> QListWidgetItem:
    """Getter-function for the hovered item"""
    if isinstance(self._hoverItem, QListWidgetItem):
      return self._hoverItem

  def _setHoverItem(self, item: QListWidgetItem) -> NoReturn:
    """Setter-function for the hovered item"""
    if isinstance(item, QListWidgetItem):
      self._hoverItem = item

  def _getClickedItem(self) -> QListWidgetItem:
    """Getter-function for the clicked item"""
    if isinstance(self._clickedItem, QListWidgetItem):
      return self._clickedItem

  def _setClickedItem(self, item: QListWidgetItem) -> NoReturn:
    """Setter-function for the clicked item"""
    if isinstance(item, QListWidgetItem):
      self._clickedItem = item

  def _getDoubleClickedItem(self) -> QListWidgetItem:
    """Getter-function for the double-clicked item"""
    if isinstance(self._doubleClickedItem, QListWidgetItem):
      return self._doubleClickedItem

  def _setDoubleClickedItem(self, item: QListWidgetItem) -> NoReturn:
    """Setter-function for the double-clicked item"""
    if isinstance(item, QListWidgetItem):
      self._doubleClickedItem = item

  @Slot(str)
  def insertText(self, label: str) -> NoReturn:
    """Inserts the given text"""
    self._logs.append(label)
    item = QListWidgetItem(label)
    QListWidget.insertItem(self, 0, item)
    self.scrollToItem(item)

  def _createBaseLayout(self) -> NoReturn:
    """Creator-function for the base layout"""
    self._baseLayout = QGridLayout()

  def _getBaseLayout(self) -> QGridLayout:
    """Getter-function for the base layout"""
    if self._baseLayout is None:
      self._createBaseLayout()
      return self._getBaseLayout()
    if isinstance(self._baseLayout, QGridLayout):
      return self._baseLayout
    raise TypeError

  def _getName(self) -> str:
    """Getter-function for the name of the instance"""
    name = maybe(self._name, 'ListWidget')
    if isinstance(name, str):
      return name
    raise TypeError

  def _setName(self, name: str) -> NoReturn:
    """Setter-function for the name of the instance"""
    self._name = name

  def _getHeader(self) -> str:
    """Getter-function for the header string"""
    return '%s contents from %s' % (self._getName(), time.ctime())

  @Slot(str)
  def saveContents(self, fileName: str) -> NoReturn:
    """Saves the logs to disk"""
    with open(fileName, 'w') as f:
      header = self._getHeader()
      data = '%s\n%s' % (header, '\n'.join(self._logs))
      f.write(data)

  def _getLogs(self) -> list[str]:
    """Getter-function for the logs"""
    if self._logs is None:
      self._logs = []
      return self._getLogs()
    if isinstance(self._logs, list):
      return self._logs
    raise TypeError

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation printing the size"""
    super().paintEvent(event)
