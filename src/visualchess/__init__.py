"""The visualchess package shows us the chess board, the chess pieces and
allows us to input chess moves visually."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.typetools import TypeBag

from ._file import File
from ._rank import Rank
from ._chesscolor import ChessColor
from ._square import Square
from ._piecetype import PieceType, OctRose, GameState
from ._settings import Settings
from ._soundeffect import SoundEffect
from ._soundenum import Sound
from ._speaker import Speaker
from ._soundenum import Sound
from ._boardlayout import BoardLayout
from ._piecegrabbingproperties import _PieceGrabbingProperties
from ._piecegrabbingoperations import _PieceGrabbingOperations
from ._piecegrabbing import PieceGrabbing
from ._checkbutton import CheckButton

from workside.widgets import CoreWidget

Widget = TypeBag(CoreWidget, BoardLayout, PieceGrabbing)
