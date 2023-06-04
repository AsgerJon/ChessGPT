"""BoardWidget is a subclass showing the chessboard"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QSize, QPointF, QRectF, Signal, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QResizeEvent, QCursor
from icecream import ic
from worktoy.core import plenty

from visualchess import BoardView, Rank, File, PieceView, BoardState, \
  Square, \
  ChessPiece
from workstyle import WhereMouse, CoreWidget

ic.configureOutput(includeContext=True)


class BoardWidget(CoreWidget):
  """BoardWidget is a subclass showing the chessboard
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  resized = Signal(QSize)
  newHover = Signal(File, Rank)
  move = Signal(QPointF)
  rightClick = Signal()

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self.setMinimumSize(QSize(400, 400))
    self._boardView = None
    self._pieceView = None
    self._parent = None
    self._rectangles = None
    self._boardRect = None
    self._hoverSquare = None
    self._hoverFile = None
    self._hoverRank = None
    self._boardState = None
    self._openHandCursor = QCursor(Qt.CursorShape.OpenHandCursor)
    self._closedHandCursor = QCursor(Qt.CursorShape.ClosedHandCursor)
    self._arrowCursor = QCursor(Qt.CursorShape.ArrowCursor)
    self.move.connect(self._moveHandle)
    self.rightClick.connect(self.debug)

  def debug(self) -> NoReturn:
    """Debugger"""
    self.getPieceView().debug()

  def _moveHandle(self, point: QPointF) -> NoReturn:
    """Handles mouse move events"""
    board = self.getBoardRect()
    mouseX = point.x() - board.left()
    mouseY = point.y() - board.top()
    x = int(mouseX / board.width() * 8)
    y = int(mouseY / board.height() * 8)
    width, height = board.width(), board.height()
    if mouseX < 0 or mouseY < 0 or mouseX > width or mouseY > height:
      self._hoverSquare = None
      self._hoverFile = None
      self._hoverRank = None
      self._boardView.clearHoverSquare()
      self.update()
      return
    file = File.byValue(x)
    rank = Rank.byValue(y)
    if not plenty(file, rank):
      return self.setCursor(self._arrowCursor)
    square = Square(file, rank)
    contents = self.getBoardState().getContents()
    if isinstance(contents, dict):
      chessPiece = contents.get(square, None)
      if isinstance(chessPiece, ChessPiece):
        self.setCursor(self._openHandCursor)
      else:
        self.setCursor(self._arrowCursor)
    if file == self._hoverFile and rank == self._hoverRank:
      return
    if file is None or rank is None:
      return
    if file is not None:
      self._hoverFile = file
    if rank is not None:
      self._hoverFile, self._hoverRank = file, rank
      self.newHover.emit(file, rank)
    self._hoverSquare = self._boardView.getSquareRect(file, rank)

  def createBoardState(self) -> NoReturn:
    """Creates the board state instance"""
    self._boardState = BoardState()

  def getBoardState(self) -> BoardState:
    """Getter-function for the board state"""
    if self._boardState is None:
      self.createBoardState()
      return self.getBoardState()
    return self._boardState

  def createBoardView(self) -> NoReturn:
    """Creator-function for boardView"""
    if self._boardView is None:
      self._boardView = BoardView(self)
      self._boardView.onUpdate(self.repaint)
      self.resized.connect(self._boardView.setViewSize)
      self.newHover.connect(self._boardView.setHoverSquare)

  def getBoardView(self) -> BoardView:
    """Getter-function for the board view"""
    if self._boardView is None:
      self.createBoardView()
      return self.getBoardView()
    if isinstance(self._boardView, BoardView):
      return self._boardView

  def createPieceView(self) -> NoReturn:
    """Creator-function for pieceView"""
    if self._pieceView is None:
      self._pieceView = PieceView(self)

  def getPieceView(self) -> PieceView:
    """Getter-function for the piece view"""
    if self._pieceView is None:
      self.createPieceView()
      return self.getPieceView()
    if isinstance(self._pieceView, PieceView):
      return self._pieceView

  def getBoardRect(self) -> QRectF:
    """Getter-function for board rect"""
    return self._boardView.getBoardRect()

  def setBoardRect(self, rect: QRectF) -> NoReturn:
    """Setter-function for board rectangle"""
    self._boardRect = rect

  def setRectangles(self, *rects) -> NoReturn:
    """Setter-function for rectangles. Triggered at the end of paint
    event."""
    self._rectangles = [*rects, ]

  def resizeEvent(self, event: QResizeEvent) -> NoReturn:
    """Resizing alerts the board view"""
    self.getBoardView().clearHoverSquare()
    self.resized.emit(event.size())
    WhereMouse.resizeEvent(self, event)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation"""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.Antialiasing)
    self.getBoardView()(painter)
    self.getPieceView()(painter)
    painter.end()

  def mouseMoveEvent(self, ):