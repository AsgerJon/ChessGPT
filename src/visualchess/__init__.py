"""The visualchess package shows us the chess board, the chess pieces and
allows us to input chess moves visually."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.typetools import TypeBag

from ._chessaudio import ChessAudio
from ._file import File
from ._rank import Rank
from ._chesscolor import ChessColor
from ._piecetype import PieceType
from ._square import Square
from ._castle import Castle
from ._chesspiece import ChessPiece
from ._move import Move
from ._settings import Settings
from ._boardstate import BoardState
from ._debugstate import DebugState
from ._chessmove import ChessMove
from ._regularmove import RegularMove
from ._kingmove import KingMove
from ._knightmove import KnightMove
from ._emptymove import Empty
from ._boardlayout import BoardLayout
from ._piecegrabbingproperties import _PieceGrabbingProperties
from ._piecegrabbingoperations import _PieceGrabbingOperations
from ._piecegrabbing import PieceGrabbing
from ._checkbutton import CheckButton

from workside.widgets import CoreWidget

Widget = TypeBag(CoreWidget, BoardLayout, PieceGrabbing)
