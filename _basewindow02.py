"""BaseWindow provides the base window of the application"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from typing import NoReturn, Never

from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout
from PySide6.QtWidgets import QWidget

from visualchess import StaticBoard, ChessPiecesWidget
from worktoyside import LayoutWidget, SpacerWidget, VerticalSpacer


#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen


class BaseWindow(QMainWindow):
  """BaseWindow provides the base window of the application
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self) -> None:
    QMainWindow.__init__(self, )
    self._windowTitle = 'ChessGPT'
    self._baseWidget = None
    self._layout = None
    self._board = None
    self._selector = None
    self._right = None
    self._left = None
    self._rightLayout = None
    self._leftLayout = None
    self._rightSpacer = None
    self._leftSpacer = None
    self.initUI()

  def getWindowTitle(self) -> str:
    """Getter-function for the window title"""
    return self._windowTitle

  def _createRight(self) -> NoReturn:
    """Creator-Function for the right widget"""
    self._right = LayoutWidget()

  def _getRight(self) -> LayoutWidget:
    """Getter-function for the right widget"""
    if self._right is None:
      self._createRight()
      return self._getRight()
    return self._right

  def _setRight(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error')

  def _delRight(self, ) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read Only Error')

  def _createRightLayout(self) -> NoReturn:
    """Creator-Function for the right widget"""
    self._rightLayout = QVBoxLayout()

  def _getRightLayout(self) -> QVBoxLayout:
    """Getter-function for the right widget"""
    if self._rightLayout is None:
      self._createRightLayout()
      return self._getRightLayout()
    return self._rightLayout

  def _setRightLayout(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error')

  def _delRightLayout(self) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read Only Error')

  def _createLeft(self) -> NoReturn:
    """Creator-Function for the left widget"""
    self._left = LayoutWidget()

  def _getLeft(self) -> LayoutWidget:
    """Getter-function for the left layoutWidget"""
    if self._left is None:
      self._createLeft()
      return self._getLeft()
    return self._left

  def _setLeft(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error')

  def _delLeft(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error')

  def _createLeftLayout(self) -> NoReturn:
    """Creator-Function for the left widget"""
    self._leftLayout = QVBoxLayout()

  def _getLeftLayout(self) -> QVBoxLayout:
    """Getter-function for the left widget"""
    if self._leftLayout is None:
      self._createLeftLayout()
      return self._getLeftLayout()
    return self._leftLayout

  def _setLeftLayout(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error')

  def _delLeftLayout(self) -> Never:
    """Illegal deleter function"""

  def _createRightSpacer(self) -> NoReturn:
    """Creator-function for the right spacer"""
    self._rightSpacer = VerticalSpacer()

  def _getRightSpacer(self) -> VerticalSpacer:
    """Getter-function for the right spacer"""
    if self._rightSpacer is None:
      self._createRightSpacer()
      return self._getRightSpacer()
    return self._rightSpacer

  def _setRightSpacer(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error')

  def _delRightSpacer(self) -> Never:
    """Illegal deleter function"""

  def _createLeftSpacer(self) -> NoReturn:
    """Creator-function for the left spacer"""
    self._leftSpacer = SpacerWidget()

  def _getLeftSpacer(self) -> SpacerWidget:
    """Getter-function for the left spacer"""
    if self._leftSpacer is None:
      self._createLeftSpacer()
      return self._getLeftSpacer()
    return self._leftSpacer

  def _setLeftSpacer(self, *_) -> Never:
    """Illegal setter function"""
    raise TypeError('Read Only Error')

  def _delLeftSpacer(self) -> Never:
    """Illegal deleter function"""
    raise TypeError('Read Only Error')

  def selector(self) -> ChessPiecesWidget:
    """Getter-function for the selector"""
    if self._selector is None:
      self._selector = ChessPiecesWidget()
    return self._selector

  def createBoard(self) -> NoReturn:
    """Creator-function for the staticBoard"""
    self._board = StaticBoard()

  def board(self) -> StaticBoard:
    """Getter-function for the staticBoard"""
    if self._board is None:
      self.createBoard()
      return self.board()
    return self._board

  def initUI(self) -> NoReturn:
    """Sets up the user interface"""
    self.setWindowTitle('Chess GPT')

    self._baseWidget = QWidget(self)

    self._getRightLayout().addWidget(self.selector(), )
    self._getRightLayout().addWidget(self._getRightSpacer())

    self._getLeftLayout().addWidget(self.board())

    self._getRight().setLayout(self._getRightLayout())
    self._getLeft().setLayout(self._getLeftLayout())

    self._layout = QHBoxLayout()
    self._layout.addWidget(self._getLeft())
    self._layout.addWidget(self._getRight())

    self._baseWidget.setLayout(self._layout)

    self.setCentralWidget(self._baseWidget)
