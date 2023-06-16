"""The _PieceGrabbingProperties provides properties for the PieceGrabbing
class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QPointF, QTimer
from icecream import ic
from worktoy.waitaminute import UnexpectedStateError

from visualchess import Square, BoardLayout, GameState, PieceType
from visualchess import Settings, Sound

ic.configureOutput(includeContext=True)


class _PieceGrabbingProperties(BoardLayout):
  """This class provides the setters and getters for properties"""

  def __init__(self, *args, **kwargs) -> None:
    BoardLayout.__init__(self, *args, **kwargs)
    self._grabbedPiece = None
    self._originSquare = None
    self._boardState = None
    self._hoverSquare = None
    self._hoverPiece = None
    self._mouseX = None
    self._mouseY = None
    self._position = None
    self._mouseMoveEvent = None
    self._flagHoverBoard = None
    self._flagHoverPiece = None
    self._flagHoldingPiece = None
    self._flagMoving = None
    self._movingTimer = None
    self._gameState = None
    self._legalSquares = []
    Sound.createAll()

  ################### Mouse Position Accessor Functions ###################
  # --------------------------------------------------------------------- #
  ####################### Mouse Position as QPointF #######################
  def getMousePosition(self) -> QPointF:
    """Getter-function for mouse position"""
    return QPointF(self._mouseX, self._mouseY)

  def setMousePosition(self, mouse: QPointF) -> NoReturn:
    """Getter-function for mouse position"""
    self._position = mouse
    self._mouseX = mouse.x()
    self._mouseY = mouse.y()

  #################### END OF Mouse Position as QPointF ###################
  # --------------------------------------------------------------------- #
  ########################### Mouse x-coordinate ##########################
  def getMouseX(self) -> float:
    """Getter-function for x position"""
    return self._mouseX

  def setMouseX(self, x: float) -> NoReturn:
    """Setter-function for the x position of mouse cursor"""
    self._mouseX = x

  ####################### END OF Mouse x-coordinate #######################
  # --------------------------------------------------------------------- #
  ########################### Mouse y-coordinate ##########################
  def getMouseY(self) -> float:
    """Getter-function for x position"""
    return self._mouseY

  def setMouseY(self, y: float) -> NoReturn:
    """Setter-function for y position"""
    self._mouseY = y

  ####################### End OF Mouse y-coordinate #######################
  ################ END OF Mouse Position Accessor Functions ###############
  # --------------------------------------------------------------------- #
  ################# Accessor Functions for Chess GameState ################

  def _createGameState(self) -> NoReturn:
    """Creator-function for the game state"""
    self._gameState = GameState()

  def getGameState(self) -> GameState:
    """Getter-function for the game state"""
    if self._gameState is None:
      self._createGameState()
      return self.getGameState()
    if isinstance(self._gameState, GameState):
      return self._gameState
    raise TypeError('gameState')

  ############ END OF Accessor Functions for Chess GameState ##############
  # --------------------------------------------------------------------- #
  ######################### Hover square accessors ########################
  def getHoverSquare(self) -> Square:
    """Getter-function for hovered rectangle"""
    return self._hoverSquare

  def setHoverSquare(self, square: Square) -> NoReturn:
    """Setter-function for hovered rectangle"""
    if self._hoverSquare == square:
      return
    self._hoverSquare = square

  def delHoverSquare(self) -> NoReturn:
    """Deleter-function for the hovered rectangle"""
    if self._hoverSquare:
      self._hoverSquare = None

  ##################### END of Hover square accessors #####################
  # --------------------------------------------------------------------- #
  ######################### Hover piece Accessors #########################
  def getHoverPiece(self) -> object:
    """Getter-function for hover piece"""
    return self._hoverPiece

  def setHoverPiece(self, hoverPiece: PieceType) -> NoReturn:
    """Setter-function for hover piece"""
    if hoverPiece == self._hoverPiece:
      return
    self._hoverPiece = hoverPiece

  def delHoverPiece(self) -> NoReturn:
    """Deleter-function for hover piece"""
    if self._hoverPiece:
      self._hoverPiece = None

  ###################### END of Hover piece accessors #####################
  ################## Accessor functions for grabbed piece #################
  #########################################################################
  def getGrabbedPiece(self) -> PieceType:
    """Getter-function for the currently grabbed piece."""
    if not self._grabbedPiece:
      return PieceType.EMPTY
    if isinstance(self._grabbedPiece, PieceType):
      return self._grabbedPiece
    raise TypeError

  def setGrabbedPiece(self, piece: PieceType) -> NoReturn:
    """Getter-function for the currently grabbed piece."""
    if piece is None:
      self._grabbedPiece = PieceType.EMPTY
      return
    if isinstance(piece, PieceType):
      self._grabbedPiece = piece
      return
    raise TypeError

  def delGrabbedPiece(self) -> NoReturn:
    """Deleter-function for the grabbed piece. Returns the grabbed piece."""
    self.setGrabbedPiece(PieceType.EMPTY)

  #########################################################################
  ############## END OF Accessor functions for grabbed piece ##############
  ################## Accessor functions for origin square #################
  #########################################################################
  def getOriginSquare(self) -> Square | bool:
    """Getter-function for origin square"""
    if self._originSquare is None:
      return False
    if isinstance(self._originSquare, Square):
      return self._originSquare
    raise TypeError

  def setOriginSquare(self, square: Square) -> NoReturn:
    """Setter-function for origin square"""
    if square is None:
      raise UnexpectedStateError
    if isinstance(square, Square):
      self._originSquare = square
      return
    raise TypeError

  #########################################################################
  ############## END OF Accessor functions for origin square ##############
  #########################################################################

  #################### END OF Event Handling Functions ####################
  # --------------------------------------------------------------------- #
  ######################## Flag Accessor Functions ########################
  def getHoverBoardFlag(self) -> bool:
    """Getter-function for hover flag"""
    return True if self._flagHoverBoard else False

  def setHoverBoardFlag(self, obj: object) -> NoReturn:
    """Setter-function for hover flag. Provide any object and its boolean
    value is used."""
    self._flagHoverBoard = True if obj else False

  def getHoldingFlag(self, ) -> bool:
    """Getter-function for the holding flag. This flag should indicate
    True when a piece has been grabbed, but not yet placed or cancelled."""
    return True if self._flagHoldingPiece else False

  def setHoldingFlag(self, obj: object) -> NoReturn:
    """Setter-function for the holding flag. """
    self._flagHoldingPiece = True if obj else False

  def getHoverPieceFlag(self, ) -> bool:
    """Getter-function for the hover piece flag. This should be True when
    the mouse cursor is hovering on a square which is occupied by a
    non-empty piece."""
    return True if self._flagHoverPiece else False

  def setHoverPieceFlag(self, obj: object) -> NoReturn:
    """Setter-function for the hover piece flag."""
    self._flagHoverPiece = True if obj else False

  def _disableMovingFlag(self) -> NoReturn:
    """Explicit disabler function for moving flag."""
    self._flagMoving = False

  def _activateMovingFlag(self) -> NoReturn:
    """Explicit activator function for moving flag."""
    self._movingFlag = True
    QTimer.singleShot(Settings.movingTimeLimit, self._disableMovingFlag)

  def getMovingFlag(self, ) -> NoReturn:
    """Getter-function for the moving flag"""
    return True if self._flagMoving else False

  ##################### END OF Flag Accessor Functions ####################
