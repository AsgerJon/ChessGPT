"""The _PieceGrabbingProperties provides properties for the PieceGrabbing
class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QPointF, QTimer
from icecream import ic

from visualchess import BoardLayout, BoardState
from visualchess import Settings

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
    # Sound.createAll()

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
  ################### Accessor Functions for Chess Board ##################
  def _createBoardState(self) -> bool:
    """Creator-function for BoardState instance"""
    self._boardState = BoardState.InitialPosition()
    if isinstance(self._boardState, BoardState):
      self.update()
      return True
    raise TypeError

  def getBoardState(self) -> BoardState:
    """Getter-function for board state"""
    if self._boardState is None:
      if self._createBoardState():
        return self.getBoardState()
    if isinstance(self._boardState, BoardState):
      return self._boardState
    raise TypeError

  def resetBoardState(self, ) -> NoReturn:
    """Resets board to initial position"""
    self._boardState = BoardState.InitialPosition()
    self.update()

  ############### END OF Accessor Functions for Chess Board ###############
  # --------------------------------------------------------------------- #
  ######################### Hover square accessors ########################

  ##################### END of Hover square accessors #####################
  # --------------------------------------------------------------------- #
  ######################### Hover piece Accessors #########################

  ###################### END of Hover piece accessors #####################
  ################## Accessor functions for grabbed piece #################
  #########################################################################

  #########################################################################
  ############## END OF Accessor functions for grabbed piece ##############
  ################## Accessor functions for origin square #################
  #########################################################################

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
