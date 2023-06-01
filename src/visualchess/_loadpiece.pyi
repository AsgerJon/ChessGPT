from PIL import Image as Image, ImageQt as ImageQt
from PySide6.QtGui import QPixmap as QPixmap
from enum import IntEnum

class Piece(IntEnum):
    KING: int
    QUEEN: int
    ROOK: int
    BISHOP: int
    KNIGHT: int
    PAWN: int
    def __add__(self, other: ChessColor) -> str: ...

class ChessColor(IntEnum):
    WHITE: int
    BLACK: int
    def __add__(self, other: Piece) -> str: ...
