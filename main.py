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
from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QApplication
from icecream import ic
from worktoy.typetools import Any

from mainwindow import MainWindow
from basewindow import BaseWindow
from moreworktoy import TypeKey
from visualchess import Piece, ChessColor, loadPiece

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
  ic([*range(8)])
  ic([string.ascii_uppercase[:8]])


def tester05() -> NoReturn:
  """Testing File Enum"""


def tester06() -> NoReturn:
  """Testing torch roll"""
  lol = torch.linspace(0, 7, 8).to(torch.float32)
  print(lol)
  lol = torch.roll(lol, -1)
  print(lol)


def tester07() -> NoReturn:
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
  [newList.append(line) for _ in range(7)]

  for item in newList:
    print(item)
  print(77 * '*')
  newList[1][0][0] = 'X'
  for item in newList:
    print(item)


def tester08() -> NoReturn:
  """More reddit lulz"""
  ic(QRectF())
  ic(True if QRectF() else False)


def tester09() -> NoReturn:
  """Fuck you"""
  for piece in Piece:
    ic(piece)


def tester10() -> NoReturn:
  """lol"""
  line = string.ascii_uppercase[:8]
  num = [i ** 2 for i in range(8)]
  num2 = [2 ** i for i in range(8)]
  lol = {k: [*v, ] for (k, v) in zip(line, zip(num, num2))}
  for (key, val) in lol.items():
    print(key, val)


def tester11() -> NoReturn:
  """LOL"""
  loadPiece(Piece.BISHOP, ChessColor.WHITE)


if __name__ == '__main__':
  tester11()
  print(time.ctime())
