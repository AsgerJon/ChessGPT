"""PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
of pieces. It is divided into a properties class with getters and setters
as well as a main class with functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QEnterEvent, \
  QKeyEvent
from icecream import ic
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, BoardLayout
from visualchess import Settings, Sound, _PieceGrabbingProperties
from workstyle.stylesettings import hoveredSquareStyle

ic.configureOutput(includeContext=True)


class PieceGrabbing(_PieceGrabbingProperties):
  """PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
  of pieces. It is divided into a properties class with getters and setters
  as well as a main class with functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingProperties.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)

  # --------------------------------------------------------------------- #
  ########################## Mouse button events ##########################

  def leaveEvent(self, event: QEvent) -> NoReturn:
    """Implementation of leave event triggered when leaving the board
    rectangle. Leave events triggered by the system when the outer
    boundary is crossed, are ignored."""
    # <************************* Cancel on Leave *************************> #
    # ____________________________________________________________________
    # |  If the cursor leaves the outer square during a grabbing
    # |  operation, the operation is cancelled.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if event.type() == QEvent.Type.MouseMove:
      if self.getGrabbedPiece():
        pass
    # <********************** Remove Hover on Leave **********************> #
    # ____________________________________________________________________
    # |  When leaving the board rectangle, no square or piece should
    # |  remain hovered. This is handled by the leave method.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    self.delHoverSquare() or self.delHoverPiece()
    if event.type() == QEvent.Type.Leave:
      return super().leaveEvent(event)

  def enterEvent(self, event: QEnterEvent) -> NoReturn:
    """Implementation of enter event triggered when entering the board
    rectangle."""
    # <******************** Enter Sets Keyboard Focus ********************> #
    # ____________________________________________________________________
    # |  When entering the event it takes keyboard focus.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if not self.getBoardRect().contains(event.position()):
      self.setFocus(Qt.FocusReason.MouseFocusReason)

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """The mouse layout subclass brings the hover functionality."""
    # <*********************** Setting Hover False ***********************> #
    # ____________________________________________________________________
    # |  This is the case where the mouse has left the board rectangle. It
    # |  is triggered, the first time a move event cannot register the
    # |  event position in the board rectangle, but where the board hover
    # |  flag is still True.
    # |  In this case, the following happens:
    # |   - The board hover flag is set to False
    # |   - The mouse event received is passed on to the leave event
    # |  method
    # |   - The function returns None
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if not self.getBoardRect().contains(event.position()):
      if self.getHoverBoardFlag():
        self.setHoverBoardFlag(False)
        return self.leaveEvent(event)
      return
    # <************************ Setting Hover True ***********************> #
    # ____________________________________________________________________
    # |  This is the case where the mouse enters the board. It is
    # |  triggered whenever the move event registers the event position in
    # |  the board rectangle, but where the board hover flag is still
    # |  False.
    # |  The following happens:
    # |   - The board hover flag is set to True  - The event is
    # |  converted to an enter event
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    _enterEvent = None
    if not self.getHoverBoardFlag():
      self.setHoverBoardFlag(True)
      _enterEvent = Settings.convertToEnterEvent(self, event)
    # <*************************** Hover Square **************************> #
    # ____________________________________________________________________
    # |  Ensures that the hovered square on the board rect matches the
    # |  square in the property. If a grabbing operation is ongoing, the
    # |  method returns. If the enter event was set earlier, the event is
    # |  passed to other enter event method instead.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    square = Square.fromPointRect(event.position(), self.getBoardRect())
    self.setHoverSquare(square)
    if self.getGrabbedPiece():
      if _enterEvent is None:
        return
      if isinstance(_enterEvent, QEnterEvent):
        return self.enterEvent(_enterEvent)
      raise TypeError
    # <*************************** Hover Piece ***************************> #
    # ____________________________________________________________________
    # |  Matches the hovered piece to the piece currently marked on the
    # |  property causing an update if necessary. Please note that this
    # |  step is not reached during grabbing operations.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
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
    # <********************** Grabbing (Left-Click) **********************> #
    # ____________________________________________________________________
    # |  Triggered on left click. The method attempts to start a grabbing
    # |  operation subject to the following conditions:
    # |   - The hovered square contains a piece (not EMPTY)
    # |   - The cursor is not moving
    # |  Please note that the grabbing operation completes on the next
    # |  release event, or in case a cancelling right click is received.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if event.button() == Qt.MouseButton.LeftButton:
      hoverPiece = self.getHoverPiece()
      if not hoverPiece:
        return
      if isinstance(hoverPiece, ChessPiece):
        return self.setGrabbedPiece(hoverPiece)
      raise TypeError
    # <******************** Cancel Grab (Right-Click) ********************> #
    # ____________________________________________________________________
    # |  Cancels any ongoing grabbing operation. This is triggered when a
    # |  right click occurs after a grabbing operation has been initiated,
    # |  but before it has been completed in the release method.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if event.button() == Qt.MouseButton.RightButton:
      if self.getGrabbedPiece():
        pass

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse release event which releases the item
    either on the hovered square if allowed or back at origin square."""
    # <**************** Place Grabbed Piece (Right-Click) ****************> #
    # ____________________________________________________________________
    # |  When releasing the left mouse button any ongoing grabbing
    # |  operation completes subject to rule check. If allowable, the
    # |  grabbed piece now appears on the hovered square. If the release
    # |  occurs where no square hovered, the piece returns to its origin.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if event.button() == Qt.MouseButton.LeftButton:
      grabbedPiece = self.getGrabbedPiece()
      hoverSquare = self.getHoverSquare()
      originSquare = self.getOriginSquare()
      if not originSquare:
        return
      if grabbedPiece:
        if hoverSquare:
          self.getBoardState().setPiece(hoverSquare, grabbedPiece)
        elif originSquare:
          self.getBoardState().setPiece(originSquare, grabbedPiece)
        else:
          raise UnexpectedStateError
      self.setHoverSquare(hoverSquare)
      self.setHoverPiece(grabbedPiece)
      self.setHoverCursor()
    # <***************** Opens Context Menu (Right-Click) ****************> #
    # ____________________________________________________________________
    # |  Right-clicking when a grabbing operation is not in progress will
    # |  instead open a menu.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if event.button() == Qt.MouseButton.RightButton:
      pass  # NOT YET IMPLEMENTED

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

  def keyPressEvent(self, event: QKeyEvent) -> NoReturn:
    """Key press event implementation"""
