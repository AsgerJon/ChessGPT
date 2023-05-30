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

from mainwindow import MainWindow
from basewindow import BaseWindow
from moreworktoy import TypeKey

ic.configureOutput(includeContext=True)


def tester00() -> NoReturn:
  """Hello world"""
  for item in [time, os, sys, Any, NoReturn, BaseWindow, QApplication]:
    print(item)


def tester01() -> NoReturn:
  """Can chatgpt draw?"""
  app = QApplication([])
  main = MainWindow()
  main.show()
  app.exec()


def tester02() -> NoReturn:
  """Testing class names"""

  print('%16s' % (hash(int) - (hash(int) // 1000) * 1000))
  print('%16s' % (hash(float) - (hash(float) // 1000) * 1000))
  print('%16s' % (hash(complex) - (hash(complex) // 1000) * 1000))
  print('%16s' % (hash(str) - (hash(str) // 1000) * 1000))
  print('%16s' % (hash(type) - (hash(type) // 1000) * 1000))

  print(hash((int, str, float)))


def tester03() -> NoReturn:
  """Testing Index field"""
  lol = TypeKey(int, int, int)
  for bla in lol:
    print(bla)

  print(lol)
  ic(lol)

  ic(isinstance((1, 2, 3), lol))
  ic(isinstance((1, 2, 3.5), lol))


def tester04() -> NoReturn:
  """lol"""


if __name__ == '__main__':
  tester01()
  print(time.ctime())
