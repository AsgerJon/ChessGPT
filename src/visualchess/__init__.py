"""The visualchess package shows us the chess board, the chess pieces and
allows us to input chess moves visually."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from ._geomfuncs import fitSquareRect, fitSquareMarginsRect
from ._shade import Shade
from ._rank import Rank
from ._file import File
from ._boardview import BoardView
from ._loadpiece import Piece, ChessColor
from ._square import Square
from ._checkbutton import CheckButton
from ._boardwidget import BoardWidget
from ._widget import TestWidget
from ._squarepaint import SquarePaint
