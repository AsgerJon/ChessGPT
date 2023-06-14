"""PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
of pieces. It is divided into a properties class with getters and setters
as well as a main class with functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QEnterEvent
from PySide6.QtGui import QKeyEvent
from icecream import ic

from visualchess import ChessPiece, Square, BoardLayout
from visualchess import _PieceGrabbingOperations
from workside.styles._styleinstances import hoveredSquareStyle

ic.configureOutput(includeContext=True)


class PieceGrabbing(_PieceGrabbingOperations):
  """PieceGrabbing subclasses the MouseLayout bringing grabbing and moving
  of pieces. It is divided into a properties class with getters and setters
  as well as a main class with functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _PieceGrabbingOperations.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self.setSizePolicy(self.doubleExpand())

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
        self.cancelGrabbing()
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
    if self.getBoardRect().contains(event.position()):
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
    boardRect = self.getBoardRect()
    point = event.position()
    if not boardRect.contains(point):
      return self.leaveBoardRect(event)
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
    self.enterBoardRect(event)
    # <*************************** Hover Square **************************> #
    # ____________________________________________________________________
    # |  Ensures that the hovered square on the board rect matches the
    # |  square in the property. If a grabbing operation is ongoing, the
    # |  method returns. If the enter event was set earlier, the event is
    # |  passed to other enter event method instead.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    self.activateHoverSquare(event)
    # <*************************** Hover Piece ***************************> #
    # ____________________________________________________________________
    # |  Matches the hovered piece to the piece currently marked on the
    # |  property causing an update if necessary. Please note that this
    # |  step is not reached during grabbing operations.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

    self.activateHoverPiece(event)

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
      hoverSquare = self.getHoverSquare()
      if not hoverPiece:
        return
      if isinstance(hoverPiece, ChessPiece):
        return self.beginGrabbing(hoverPiece, hoverSquare)
      raise TypeError
    # <******************** Cancel Grab (Right-Click) ********************> #
    # ____________________________________________________________________
    # |  Cancels any ongoing grabbing operation. This is triggered when a
    # |  right click occurs after a grabbing operation has been initiated,
    # |  but before it has been completed in the release method.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    if event.button() == Qt.MouseButton.RightButton:
      self.cancelGrabbing()

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
      self.completeGrabbing()
      return self.update()

    # <***************** Opens Context Menu (Right-Click) ****************> #
    # ____________________________________________________________________
    # |  Right-clicking when a grabbing operation is not in progress will
    # |  instead open a menu.
    # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

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
