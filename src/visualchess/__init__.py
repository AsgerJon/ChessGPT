"""The visualchess package shows us the chess board, the chess pieces and
allows us to input chess moves visually."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.typetools import TypeBag

from ._settings import Settings
from ._soundeffect import SoundEffect
from ._soundenum import Sound
from ._speaker import Speaker
from ._soundenum import Sound
from ._enums import File, Rank, ChessColor, PieceType
from ._square import Square
from ._move import PieceMove
from ._chesspiece import ChessPiece
from ._boardstate import BoardState
from ._debugstate import DebugState
from ._boardlayout import BoardLayout
from ._piecegrabbingproperties import _PieceGrabbingProperties
from ._piecegrabbingoperations import _PieceGrabbingOperations
from ._piecegrabbing import PieceGrabbing
from ._loadpiece import Piece, ChessColor, loadPiece
from ._checkbutton import CheckButton

from workside.widgets import CoreWidget

Widget = TypeBag(CoreWidget, BoardLayout, PieceGrabbing)
