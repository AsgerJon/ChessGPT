"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt
from icecream import ic
from worktoy.core import maybe

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

  def show(self) -> NoReturn:
    """Reimplementation of show method"""
    LayoutWindow.show(self)
    self.setupActions()

  def setupActions(self) -> NoReturn:
    """Sets up the actions"""
    self._getDebugButton().leftPressHold.connect(self.handleLeftPressHold)

  def handleLeftPressHold(self) -> NoReturn:
    """Handles the left press hold signal"""
    self._getBoardWidget().getBoardState().resetInitialPosition()
    self._getBoardWidget().update()

  def debugFunc01(self) -> NoReturn:
    """omg"""
    board = self._getBoardWidget()
    names = ['__name__', '__class__', '__mro__', '__bases__']
    for name in names:
      print(maybe(getattr(board, name, None), '%s not found' % name))

  def debugFunc02(self) -> NoReturn:
    """omg"""

  def debugFunc03(self) -> NoReturn:
    """omg"""

  def debugFunc04(self) -> NoReturn:
    """omg"""
