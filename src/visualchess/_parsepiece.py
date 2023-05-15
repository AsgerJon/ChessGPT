"""The parsePiece function parses string arguments to identify the piece"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import stringList, maybeTypes


def parsePiece(*args, **kwargs) -> tuple[str, str]:
  """The parsePiece function parses string arguments to identify the piece
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  strArgs = maybeTypes(str, *args)
  pieceColor, pieceName = None, None
  data = ' '.join(strArgs)
  for color in stringList('light, dark, white, black'):
    for piece in stringList('king, queen, rook, bishop, knight, pawn'):
      if color in data and pieceColor is None:
        pieceColor = color
      if piece in data and pieceName is None:
        pieceName = piece
      if pieceName is not None and pieceColor is not None:
        break
    if pieceName is not None and pieceColor is not None:
      break
  return (pieceColor, pieceName)
