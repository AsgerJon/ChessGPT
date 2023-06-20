"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

import chess
import chess.svg
from icecream import ic

from workside.audio import Sound
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
    Sound.error.play()

  def debugFunc02(self) -> NoReturn:
    """omg"""
    img = chess.svg.board(self._getBoardWidget().getBoardState().board)
    print(type(img))

  def debugFunc03(self) -> NoReturn:
    """omg"""
    img = chess.svg.board(self._getBoardWidget().getBoardState().board)
    with open('lol.svg', 'w') as f:
      f.write(img)

  def debugFunc04(self) -> NoReturn:
    """omg"""
