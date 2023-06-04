"""Square instances represent squares on the chess board"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF
from icecream import ic
from worktoy.parsing import maybeType, extractArg
from worktoy.stringtools import stringList

from visualchess import File, Rank
from workstyle.styles import BoardDims

ic.configureOutput(includeContext=True)


class Square:
  """Square instances represent squares on the chess board.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    fileKeys = stringList('file, column, x')
    rankKeys = stringList('rank, row, y')
    self._file, a, k = extractArg(File, fileKeys, *args, **kwargs)
    self._rank, a, k = extractArg(Rank, rankKeys, *args, **kwargs)

  def rect(self) -> QRectF:
    grid = int(BoardDims.gridPixels)
