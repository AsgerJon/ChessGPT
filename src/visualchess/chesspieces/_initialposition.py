"""This file contains code setting up the initial position"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.stringtools import stringList

ic.configureOutput(includeContext=True)

initialPosition = [
  stringList('A1, white, rook'),
  stringList('B1, white, knight'),
  stringList('C1, white, bishop'),
  stringList('D1, white, queen'),
  stringList('E1, white, king'),
  stringList('F1, white, bishop'),
  stringList('G1, white, knight'),
  stringList('H1, white, rook'),
  stringList('A2, white, pawn'),
  stringList('B2, white, pawn'),
  stringList('C2, white, pawn'),
  stringList('D2, white, pawn'),
  stringList('E2, white, pawn'),
  stringList('F2, white, pawn'),
  stringList('G2, white, pawn'),
  stringList('H2, white, pawn'),
  stringList('A8, black, rook'),
  stringList('B8, black, knight'),
  stringList('C8, black, bishop'),
  stringList('D8, black, queen'),
  stringList('E8, black, king'),
  stringList('F8, black, bishop'),
  stringList('G8, black, knight'),
  stringList('H8, black, rook'),
  stringList('A7, black, pawn'),
  stringList('B7, black, pawn'),
  stringList('C7, black, pawn'),
  stringList('D7, black, pawn'),
  stringList('E7, black, pawn'),
  stringList('F7, black, pawn'),
  stringList('G7, black, pawn'),
  stringList('H7, black, pawn'),
]
