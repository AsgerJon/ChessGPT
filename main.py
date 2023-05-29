"""Main Tester Script"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
from typing import NoReturn

from PySide6.QtWidgets import QApplication
from worktoy.typetools import Any

from _basewindow02 import BaseWindow


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


if __name__ == '__main__':
  tester01()
  print(time.ctime())
