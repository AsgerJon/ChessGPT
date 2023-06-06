"""The visualchess package shows us the chess board, the chess pieces and
allows us to input chess moves visually."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.typetools import TypeBag
from workstyle import CoreWidget

from ._settings import Settings
from ._speaker import Speaker
from ._soundboard import SoundBoard
from ._soundenum import Sound
from ._enums import File, Rank, ChessPiece, Square, BoardState
from ._boardlayout import BoardLayout
from ._mouselayout import MouseLayout
from ._piecegrabbing import PieceGrabbing
from ._loadpiece import Piece, ChessColor, loadPiece
from ._checkbutton import CheckButton

Widget = TypeBag(CoreWidget, BoardLayout, MouseLayout, PieceGrabbing)
