"""Main Tester Script"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtWidgets import QApplication

from _basewindow import BaseWindow


def tester00() -> NoReturn:
  """Hello world"""
  for item in []:
    print(item)


def tester01() -> NoReturn:
  """Can chatgpt draw?"""


def tester02() -> NoReturn:
  """Testing a basic application with a single window"""
  app = QApplication([])
  window = BaseWindow()
  window.show()
  app.exec()


def tester03() -> NoReturn:
  """Renaming chess pieces"""
  here = os.path.dirname(os.path.abspath(__file__))
  dirName = os.path.join(here, 'src', 'visualchess', 'images')
  chessPieces = []


def tester04() -> NoReturn:
  """Fizz Buzz"""
  for i in range(1, 101):
    print('%s%s' % ('' if i % 5 else 'Fizz', '' if i % 3 else 'Buzz') or i)


if __name__ == '__main__':
  tester04()
