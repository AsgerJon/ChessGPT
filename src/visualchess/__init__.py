"""The visualchess package shows us the chess board, the chess pieces and
allows us to input chess moves visually."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._parsepiece import parsePiece
from ._showpiece import showPiece
from ._pieceselector import ChessPiecesWidget
from ._square import Piece, Square
from ._staticboard import StaticBoard
