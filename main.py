"""Main Tester Script"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import string
import sys
import time
from typing import NoReturn

import torch
from PySide6.QtCore import QRectF, QPointF
from PySide6.QtWidgets import QApplication
from icecream import ic
from worktoy.typetools import Any

from basewindow import BaseWindow
from mainwindow import MainWindow
from moreworktoy import TypeKey
from visualchess import Piece
from workstyle import GameWindow

ic.configureOutput(includeContext=True)


def tester00() -> None:
  """Hello world"""
  for item in [time, os, sys, Any, NoReturn, BaseWindow, QApplication]:
    print(item)


def tester01() -> None:
  """Can chatgpt draw?"""
  app = QApplication([])
  main = MainWindow()
  main.show()
  app.exec()


def tester02() -> None:
  """Testing class names"""

  print('%16s' % (hash(int) - (hash(int) // 1000) * 1000))
  print('%16s' % (hash(float) - (hash(float) // 1000) * 1000))
  print('%16s' % (hash(complex) - (hash(complex) // 1000) * 1000))
  print('%16s' % (hash(str) - (hash(str) // 1000) * 1000))
  print('%16s' % (hash(type) - (hash(type) // 1000) * 1000))

  print(hash((int, str, float)))


def tester03() -> None:
  """Testing Index field"""
  lol = TypeKey(int, int, int)
  for bla in lol:
    print(bla)

  print(lol)
  ic(lol)

  ic(isinstance((1, 2, 3), lol))
  ic(isinstance((1, 2, 3.5), lol))


def tester04() -> None:
  """lol"""
  ic([*range(8)])
  ic([string.ascii_uppercase[:8]])


def tester05() -> None:
  """Testing File Enum"""
  app = QApplication([])
  main = GameWindow()
  main.show()
  app.exec()


def tester06() -> None:
  """Testing torch roll"""
  lol = torch.linspace(0, 7, 8).to(torch.float32)
  print(lol)
  lol = torch.roll(lol, -1)
  print(lol)


def tester07() -> None:
  """Reddit distractions"""

  board_matrix = [
    [['E', (None, None)], ['E', (None, None)], ['E', (None, None)],
     ['E', (None, None)], ['E', (None, None)], ['E', (None, None)]],

    [['E', (None, None)], ['E', (None, None)], ['E', (None, None)],
     ['E', (None, None)], ['E', (None, None)], ['E', (None, None)]],

    [['E', (None, None)], ['E', (None, None)], ['E', (None, None)],
     ['E', (None, None)], ['E', (None, None)], ['E', (None, None)]],

    [['E', (None, None)], ['E', (None, None)], ['E', (None, None)],
     ['E', (None, None)], ['E', (None, None)], ['E', (None, None)]],

    [['E', (None, None)], ['E', (None, None)], ['E', (None, None)],
     ['E', (None, None)], ['E', (None, None)], ['E', (None, None)]],

    [['E', (None, None)], ['E', (None, None)], ['E', (None, None)],
     ['E', (None, None)], ['E', (None, None)], ['E', (None, None)]],

    [['E', (None, None)], ['E', (None, None)], ['E', (None, None)],
     ['E', (None, None)], ['E', (None, None)], ['E', (None, None)]]]

  line = board_matrix[0]

  newList = []
  for _ in range(7):
    newList.append(line)

  for item in newList:
    print(item)
  print(77 * '*')
  newList[1][0][0] = 'X'
  for item in newList:
    print(item)


def tester08() -> None:
  """More reddit lulz"""
  ic(QRectF())
  ic(True if QRectF() else False)


def tester09() -> None:
  """Fuck you"""
  for piece in Piece:
    ic(piece)


def tester10() -> None:
  """lol"""
  line = string.ascii_uppercase[:8]
  num = [i ** 2 for i in range(8)]
  num2 = [2 ** i for i in range(8)]
  lol = {k: [*v, ] for (k, v) in zip(line, zip(num, num2))}
  for (key, val) in lol.items():
    print(key, val)


def tester11() -> None:
  """LOL"""
  rect = QRectF(QPointF(0, 0), QPointF(16, 16))
  ic(rect)
  rect.adjust(-2, 0, -2, -2)
  ic(rect)


if __name__ == '__main__':
  tester01()
  print(time.ctime())
