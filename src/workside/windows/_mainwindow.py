"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt
from icecream import ic

from visualchess import ChessPiece
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

  def setupActions(self) -> NoReturn:
    """Sets up the actions"""
    self._getDebugButton().leftPressHold.connect(
      self._getBoardWidget().resetBoardState)

  def show(self, ) -> NoReturn:
    """Reimplementation"""
    LayoutWindow.show(self)
    self.setupActions()

  def debugFunc01(self) -> NoReturn:
    """omg"""
    self._getBoardWidget().getBoardState().debug()

  def debugFunc02(self) -> NoReturn:
    """omg"""

  def debugFunc03(self) -> NoReturn:
    """omg"""

  def debugFunc04(self) -> NoReturn:
    """omg"""
