"""BaseWindow"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence

from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QKeyEvent, QKeySequence
from PySide6.QtWidgets import QMainWindow, QLabel, QSizePolicy, QWidget


class BaseWindow(QMainWindow):
  """A subclass of QMainWindow that provides menus and actions for a simple
  word processing application.

  This class creates File and Edit menus with basic actions for creating,
  opening, saving, cutting, copying, and pasting files.
  You can add more widgets and layouts to this subclass later on to create
  your word processing application."""

  spaceKeyRelease = Signal()
  spaceKeyPress = Signal()

  def __init__(self, parent: QWidget = None) -> None:
    QMainWindow.__init__(self, parent)
    self.setMouseTracking(True)
    statusBar = QLabel()
    policy = QSizePolicy()
    policy.setVerticalPolicy(QSizePolicy.Policy.Maximum)
    policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
    statusBar.setSizePolicy(policy)
    self.statusBar().addWidget(statusBar)

    # Create menus
    fileMenu = self.menuBar().addMenu("&File")
    editMenu = self.menuBar().addMenu("&Edit")
    helpMenu = self.menuBar().addMenu("&Help")

    # Create actions
    newAction = QAction("&New", self)
    openAction = QAction("&Open", self)
    saveAction = QAction("&Save", self)
    saveAsAction = QAction("Save &As...", self)
    exitAction = QAction("&Exit", self)

    cutAction = QAction("Cu&t", self)
    copyAction = QAction("&Copy", self)
    pasteAction = QAction("&Paste", self)

    # Add actions to menus
    fileMenu.addAction(newAction)
    fileMenu.addAction(openAction)
    fileMenu.addAction(saveAction)
    fileMenu.addAction(saveAsAction)
    fileMenu.addSeparator()
    fileMenu.addAction(exitAction)

    editMenu.addAction(cutAction)
    editMenu.addAction(copyAction)
    editMenu.addAction(pasteAction)

    # Connect signals and slots
    newAction.triggered.connect(self.newFile)
    openAction.triggered.connect(self.openFile)
    saveAction.triggered.connect(self.saveFile)
    saveAsAction.triggered.connect(self.saveFileAs)
    exitAction.triggered.connect(self.close)

    cutAction.triggered.connect(self.cut)
    copyAction.triggered.connect(self.copy)
    pasteAction.triggered.connect(self.paste)

    self.debugAction01 = QAction("Debug 01", self)
    self.debugAction02 = QAction("Debug 02", self)
    self.debugAction03 = QAction("Debug 03", self)
    self.debugAction04 = QAction("Debug 04", self)
    self.debugAction05 = QAction("Debug 05", self)
    self.debugAction06 = QAction("Debug 06", self)
    self.debugAction07 = QAction("Debug 07", self)
    self.debugAction08 = QAction("Debug 08", self)
    self.debugAction09 = QAction("Debug 09", self)
    self.debugAction10 = QAction("Debug 10", self)
    self.debugAction11 = QAction("Debug 11", self)
    self.debugAction12 = QAction("Debug 12", self)
    helpMenu.addAction(self.debugAction01)
    helpMenu.addAction(self.debugAction02)
    helpMenu.addAction(self.debugAction03)
    helpMenu.addAction(self.debugAction04)
    helpMenu.addAction(self.debugAction05)
    helpMenu.addAction(self.debugAction06)
    helpMenu.addAction(self.debugAction07)
    helpMenu.addAction(self.debugAction08)
    helpMenu.addAction(self.debugAction09)
    helpMenu.addAction(self.debugAction10)
    helpMenu.addAction(self.debugAction11)
    helpMenu.addAction(self.debugAction12)

  def show(self) -> NoReturn:
    """Sets up debuggers"""
    self.setupDebuggers()
    QMainWindow.show(self)

  def setupDebuggers(self) -> NoReturn:
    """Setting up the actions"""
    self.debugAction01.setShortcut(QKeySequence.fromString('F1'))
    self.debugAction01.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction01.triggered.connect(self.debugFunc01)

    self.debugAction02.setShortcut(QKeySequence.fromString('F2'))
    self.debugAction02.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction02.triggered.connect(self.debugFunc02)

    self.debugAction03.setShortcut(QKeySequence.fromString('F3'))
    self.debugAction03.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction03.triggered.connect(self.debugFunc03)

    self.debugAction04.setShortcut(QKeySequence.fromString('F4'))
    self.debugAction04.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction04.triggered.connect(self.debugFunc04)

    self.debugAction05.setShortcut(QKeySequence.fromString('F5'))
    self.debugAction05.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction05.triggered.connect(self.debugFunc05)

    self.debugAction06.setShortcut(QKeySequence.fromString('F6'))
    self.debugAction06.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction06.triggered.connect(self.debugFunc06)

    self.debugAction07.setShortcut(QKeySequence.fromString('F7'))
    self.debugAction07.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction07.triggered.connect(self.debugFunc07)

    self.debugAction08.setShortcut(QKeySequence.fromString('F8'))
    self.debugAction08.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction08.triggered.connect(self.debugFunc08)

    self.debugAction09.setShortcut(QKeySequence.fromString('F9'))
    self.debugAction09.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction09.triggered.connect(self.debugFunc09)

    self.debugAction10.setShortcut(QKeySequence.fromString('F10'))
    self.debugAction10.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction10.triggered.connect(self.debugFunc10)

    self.debugAction11.setShortcut(QKeySequence.fromString('F11'))
    self.debugAction11.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction11.triggered.connect(self.debugFunc11)

    self.debugAction12.setShortcut(QKeySequence.fromString('F12'))
    self.debugAction12.setShortcutContext(
      Qt.ShortcutContext.ApplicationShortcut)
    self.debugAction12.triggered.connect(self.debugFunc12)

  def keyReleaseEvent(self, event: QKeyEvent) -> NoReturn:
    """Triggers spell checking"""
    QMainWindow.keyReleaseEvent(self, event)

  def keyPressEvent(self, event: QKeyEvent) -> NoReturn:
    """Triggers spell checking"""
    QMainWindow.keyPressEvent(self, event)

  def debugFunc01(self) -> NoReturn:
    """Debugger 01"""

  def debugFunc02(self) -> NoReturn:
    """Debugger 02"""

  def debugFunc03(self) -> NoReturn:
    """Debugger 03"""

  def debugFunc04(self) -> NoReturn:
    """Debugger 04"""

  def debugFunc05(self) -> NoReturn:
    """Debugger 05"""

  def debugFunc06(self) -> NoReturn:
    """Debugger 06"""

  def debugFunc07(self) -> NoReturn:
    """Debugger 07"""

  def debugFunc08(self) -> NoReturn:
    """Debugger 08"""

  def debugFunc09(self) -> NoReturn:
    """Debugger 09"""

  def debugFunc10(self) -> NoReturn:
    """Debugger 10"""

  def debugFunc11(self) -> NoReturn:
    """Debugger 11"""

  def debugFunc12(self) -> NoReturn:
    """Debugger 12"""

  # Define slots
  def newFile(self) -> NoReturn:
    """Creates a new file."""

  def openFile(self) -> NoReturn:
    """Opens an existing file."""

  def saveFile(self) -> NoReturn:
    """Saves the current file"""

  def saveFileAs(self) -> NoReturn:
    """Saves the current file with a new name"""

  def cut(self) -> NoReturn:
    """Cuts the selected text"""

  def copy(self) -> NoReturn:
    """Copies the selected text"""

  def paste(self) -> NoReturn:
    """Pastes the copied or cut text"""
