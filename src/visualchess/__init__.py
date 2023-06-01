"""The visualchess package shows us the chess board, the chess pieces and
allows us to input chess moves visually."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._loadpiece import Piece, ChessColor, loadPiece
from ._enums import File, Rank
from ._square import Square
from ._chessboardfunc import chessBoardFunc
from ._checkbutton import CheckButton
from ._staticboard import StaticBoard
from ._widget import TestWidget
