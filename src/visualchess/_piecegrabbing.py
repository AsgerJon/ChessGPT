"""PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
of pieces. It is divided into a properties class with getters and setters
as well as a main class with functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from icecream import ic

from visualchess import MouseLayout, ChessPiece, Square

ic.configureOutput(includeContext=True)


class _PieceGrabbingProperties(MouseLayout):
  """This class provides the setters and getters for properties"""

  def __init__(self, *args, **kwargs) -> None:
    MouseLayout.__init__(self, *args, **kwargs)


class PieceGrabbing(_PieceGrabbingProperties):
  """PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
  of pieces. It is divided into a properties class with getters and setters
  as well as a main class with functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  grabbedPiece = Signal(ChessPiece, )
  clearSquare = Signal(Square)
  placePieceSquare = Signal(Square)

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)
