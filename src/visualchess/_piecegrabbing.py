"""PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
of pieces. It is divided into a properties class with getters and setters
as well as a main class with functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Signal, Qt, QPointF, QEvent, QTimer
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QEnterEvent
from icecream import ic
from worktoy.parsing import maybeType
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, BoardState, BoardLayout, Settings
from workstyle.stylesettings import hoveredSquareStyle

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
    self._flagHoverBoard = None
    self._flagHoverPiece = None
    self._flagHoldingPiece = None
    self._flagMoving = None
    self._movingTimer = None

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

  ############### END OF Accessor Functions for Chess Board ###############
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

  def setHoverPiece(self, hoverPiece: ChessPiece) -> NoReturn:
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
  def getGrabbedPiece(self) -> ChessPiece:
    """Getter-function for the currently grabbed piece."""
    if self._grabbedPiece is None:
      return ChessPiece.EMPTY
    if isinstance(self._grabbedPiece, ChessPiece):
      return self._grabbedPiece
    raise TypeError

  def setGrabbedPiece(self, piece: ChessPiece) -> NoReturn:
    """Getter-function for the currently grabbed piece."""
    if piece is None:
      self._grabbedPiece = ChessPiece.EMPTY
      return
    if isinstance(piece, ChessPiece):
      self._grabbedPiece = piece
      return
    raise TypeError

  def delGrabbedPiece(self) -> ChessPiece:
    """Deleter-function for the grabbed piece. Returns the grabbed piece."""
    piece = self.getGrabbedPiece()
    self.setGrabbedPiece(ChessPiece.EMPTY)
    return piece

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


class _PieceGrabbingSignals(_PieceGrabbingProperties):
  """In between class for signal handling functions"""

  alertChangeHoverSquare = Signal(Square)
  alertClearHoverSquare = Signal()
  alertChangeHoverPiece = Signal(ChessPiece)
  alertClearHoverPiece = Signal()
  alertGrabbedPiece = Signal(ChessPiece)
  alertDroppedPiece = Signal(ChessPiece)
  alertClearedSquare = Signal(Square)
  alertPiecePlaced = Signal(ChessPiece, Square)
  alertCancelMove = Signal()
  alertMovingStopped = Signal()
  soundPiecePlaced = Signal()
  soundPiecePicked = Signal()
  soundPieceMoved = Signal()

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)


class PieceGrabbing(_PieceGrabbingSignals):
  """PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
  of pieces. It is divided into a properties class with getters and setters
  as well as a main class with functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingSignals.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self.alertGrabbedPiece.connect(self.handleGrabbedPiece)
    self.alertDroppedPiece.connect(self.handleDroppedPiece)
    self.alertClearedSquare.connect(self.handleClearedSquare)
    self.alertPiecePlaced.connect(self.handlePiecePlaced)
    self.alertChangeHoverSquare.connect(self.handleChangeHoverSquare)
    self.alertClearHoverSquare.connect(self.handleClearHoverSquare)
    self.alertChangeHoverPiece.connect(self.handleChangeHoverPiece)
    self.alertClearHoverPiece.connect(self.handleClearHoverPiece)

  ######################## Event Handling Functions #######################
  def handleChangeHoverSquare(self, square: Square) -> NoReturn:
    """Handles changes to hover square"""
    if not isinstance(square, Square):
      raise TypeError
    self.update()

  def handleClearHoverSquare(self, *square: Square) -> NoReturn:
    """Handles the clearing of the hover square"""
    square = maybeType(Square, *square)
    if square is None or isinstance(square, Square):
      self.update()

  def handleChangeHoverPiece(self, piece: ChessPiece = None) -> NoReturn:
    """Handles changes to the piece being hovered"""
    self.setCursor(Qt.CursorShape.OpenHandCursor)
    self.update()

  def handleClearHoverPiece(self) -> NoReturn:
    """Clears the hover piece func"""
    self.setCursor(Qt.CursorShape.ArrowCursor)
    self.update()

  def handleGrabbedPiece(self, piece: ChessPiece) -> NoReturn:
    """Handles the piece grabbing signal"""
    self.soundPiecePicked.emit()
    self.setGrabbedPiece(piece)
    square = self.getHoverSquare()
    self.setOriginSquare(square)
    self.delHoverPiece()
    self.setPieceCursor(piece)
    self.getBoardState().setPiece(square, ChessPiece.EMPTY)

  def handleDroppedPiece(self, piece: ChessPiece) -> NoReturn:
    """Handles the piece dropping signal"""

  def handleClearedSquare(self, square: Square) -> NoReturn:
    """Handles clear square signal"""

  def handlePiecePlaced(self, piece: ChessPiece, square: Square) -> NoReturn:
    """Handles piece placed signal"""
    self.soundPiecePlaced.emit()
    self.getBoardState().setPiece(square, piece)
    if self.getBoardState().getPiece(square) == piece:
      self.delGrabbedPiece()

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
  # --------------------------------------------------------------------- #
  ########################## Mouse button events ##########################

  def leaveEvent(self, event: QEvent) -> NoReturn:
    """Implementation of leave event triggered when leaving the board
    rectangle. Leave events triggered by the system when the outer
    boundary is crossed, are ignored."""
    if event.type() == QEvent.Type.MouseMove:
      self.delHoverSquare() or self.delHoverPiece()

    if event.type() == QEvent.Type.Leave:
      return super().leaveEvent(event)

  def enterEvent(self, event: QEnterEvent) -> NoReturn:
    """Implementation of enter event triggered when entering the board
    rectangle."""

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """The mouse layout subclass brings the hover functionality."""
    if not self.getBoardRect().contains(event.position()):
      if self.getHoverBoardFlag():
        self.setHoverBoardFlag(False)
        return self.leaveEvent(event)
      return
    if not self.getHoverBoardFlag():
      raise NotImplementedError

    square = Square.fromPointRect(event.position(), self.getBoardRect())
    self.setHoverSquare(square)
    if self.getGrabbedPiece():
      return
    hoverPiece = self.getBoardState().getPiece(square)
    if not hoverPiece:
      if self.getHoverPiece():
        return self.delHoverPiece()
      return
    if self.getHoverPiece() == hoverPiece:
      return
    self.setHoverPiece(hoverPiece)

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse press event grabs the piece on the hovered
    square if available."""
    if event.button() == Qt.MouseButton.LeftButton:
      hoverPiece = self.getHoverPiece()
      if not hoverPiece:
        return
      self.alertGrabbedPiece.emit(hoverPiece)
    if event.button() == Qt.MouseButton.RightButton:
      if self.getGrabbedPiece():
        self.alertCancelMove.emit()

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse release event which releases the item
    either on the hovered square if allowed or back at origin square."""
    if event.button() == Qt.MouseButton.LeftButton:
      grabbedPiece = self.getGrabbedPiece()
      hoverSquare = self.getHoverSquare()
      originSquare = self.getOriginSquare()
      if not originSquare:
        return
      if grabbedPiece:
        if hoverSquare:
          self.alertPiecePlaced.emit(grabbedPiece, hoverSquare)
        elif originSquare:
          self.alertPiecePlaced.emit(grabbedPiece, originSquare)
        else:
          raise UnexpectedStateError
      self.setHoverSquare(hoverSquare)
      self.setHoverPiece(grabbedPiece)
      self.setHoverCursor()

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """The MouseLayout subclass provides the painting of chess pieces and
    the hovering functionality."""
    BoardLayout.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    if self.getHoverSquare():
      hoveredSquareStyle @ painter
      painter.drawRect(self.getHoverSquare() @ self.getBoardRect())
    for (square, piece) in self.getBoardState().items():
      if isinstance(square, Square):
        target = square @ self.getBoardRect()
        if isinstance(piece, ChessPiece):
          if piece:
            pix = piece.getPixmap()
            source = pix.rect().toRectF()
            painter.drawPixmap(target, pix, source)
    painter.end()
