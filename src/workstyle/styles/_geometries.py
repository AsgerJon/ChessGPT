"""This file specifies geometric information about the static chessboard
such as relative bezels and gridlines"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


class BoardDims:
  """Board dimensions"""
  bezelRatio = 32 / 400
  boardRatio = 1 - bezelRatio
  gridRatio = 8 / 400
