"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt
from icecream import ic

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

  def debugFunc01(self) -> NoReturn:
    """omg"""
    self._getToggleButton()._getMovingDelayTimer().start()
    if self._getToggleButton()._getMovingDelayTimer().isActive():
      print('active')

  def debugFunc02(self) -> NoReturn:
    """omg"""
    self._getToggleButton().movingActivated.emit()

  def debugFunc03(self) -> NoReturn:
    """omg"""
    print(self._getDebugButton()._getLeftButton(
    )._getDoubleClickLockoutTimer().remainingTime())

  def debugFunc04(self) -> NoReturn:
    """omg"""
    print(self._getDebugButton()._getLeftButton(
    )._getDoubleClickLockoutTimer().start())
