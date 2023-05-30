"""Main Tester Script"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
from typing import NoReturn

from PySide6.QtWidgets import QApplication
from icecream import ic
from worktoy.typetools import Any

from basewindow import BaseWindow
from moreworktoy import _ClassNames

ic.configureOutput(includeContext=True)


def tester00() -> NoReturn:
  """Hello world"""
  for item in [time, os, sys, Any, NoReturn, BaseWindow, QApplication]:
    print(item)


def tester01() -> NoReturn:
  """Can chatgpt draw?"""
  app = QApplication(sys.argv)
  main = BaseWindow()
  main.show()
  sys.exit(app.exec())


def tester02() -> NoReturn:
  """Testing class names"""
  lol = _ClassNames(['lol', 1, 2, 3, 'blabla'])
  ic(lol)
  ic(type(lol))


if __name__ == '__main__':
  tester02()
  print(time.ctime())
