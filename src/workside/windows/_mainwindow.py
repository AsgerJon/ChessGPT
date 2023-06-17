"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt
from icecream import ic
from worktoy.core import maybe

from visualchess import ChessPiece, Sound
from workside.windows import LayoutWindow

ic.configureOutput(includeContext=True)


class MainWindow(LayoutWindow):
  """MainWindow
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, ) -> None:
    LayoutWindow.__init__(self)
    self.setMinimumWidth(480)
    self.setMinimumHeight(640)
    self.setWindowTitle('Welcome to WorkSide!')

  def show(self) -> NoReturn:
    """Reimplementation of show method"""
    LayoutWindow.show(self)
    self.setupActions()

  def setupActions(self) -> NoReturn:
    """Sets up the actions"""
    self._getDebugButton().leftPressHold.connect(self.handleLeftPressHold)
    self._getDebugButton2().leftPressHold.connect(self.handleLeftPressHold2)

  def handleLeftPressHold(self) -> NoReturn:
    """Handles the left press hold signal"""
    self._getBoardWidget().getBoardState().resetInitialPosition()
    self._getBoardWidget().update()

  def handleLeftPressHold2(self) -> NoReturn:
    """Handles the left press hold signal"""
    Sound.right2jail_rightaway.play()

  def debugFunc01(self) -> NoReturn:
    """omg"""
    print(self._getDebugButton().__name__)
    print(self._getDebugButton2().__name__)

  def debugFunc02(self) -> NoReturn:
    """omg"""
    self.setupActions()
    self.update()
    print('debug2')

  def debugFunc03(self) -> NoReturn:
    """omg"""

  def debugFunc04(self) -> NoReturn:
    """omg"""
