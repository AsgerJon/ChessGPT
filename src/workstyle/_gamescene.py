#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Qt, QRectF, QMimeData, QPoint, QByteArray
from PySide6.QtGui import QDrag, QPixmap, QPainter


class DraggableRectItem(QGraphicsRectItem):
  def __init__(self, x, y, width, height, color):
    super().__init__(QRectF(x, y, width, height))
    self.setBrush(color)
    self.setFlag(QGraphicsRectItem.ItemIsMovable)
    self.setAcceptDrops(True)

  def dragEnterEvent(self, event):
    if event.mimeData().hasFormat("application/x-gamepiece"):
      event.acceptProposedAction()

  def dragMoveEvent(self, event):
    if event.mimeData().hasFormat("application/x-gamepiece"):
      event.acceptProposedAction()

  def dropEvent(self, event):
    if event.mimeData().hasFormat("application/x-gamepiece"):
      pos = event.scenePos()
      self.setPos(pos)


class GameScene(QGraphicsScene):
  def __init__(self, parent=None):
    super().__init__(parent)

    self.setSceneRect(0, 0, 800, 600)  # Set the size of the scene

    # Create and add game pieces to the scene
    self.createGamePiece(100, 100, 50, 50, Qt.red)
    self.createGamePiece(200, 200, 50, 50, Qt.green)
    self.createGamePiece(300, 300, 50, 50, Qt.blue)

  def createGamePiece(self, x, y, width, height, color):
    game_piece = DraggableRectItem(x, y, width, height, color)
    self.addItem(game_piece)

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      items = self.items(event.scenePos())
      if items:
        self.selected_item = items[0]
        self.start_pos = event.scenePos()

  def mouseMoveEvent(self, event):
    if self.selected_item is not None:
      if (event.scenePos() - self.start_pos).manhattanLength() >= 10:
        drag = QDrag(event.widget())
        mime_data = QMimeData()
        mime_data.setData("application/x-gamepiece", QByteArray())
        drag.setMimeData(mime_data)
        pixmap = QPixmap(self.selected_item.boundingRect().size().toSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.selected_item.paint(painter, None, None)
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos() - self.selected_item.pos().toPoint())
        drag.exec_(Qt.MoveAction)

  def dragEnterEvent(self, event):
    if event.mimeData().hasFormat("application/x-gamepiece"):
      event.acceptProposedAction()

  def dragMoveEvent(self, event):
    if event.mimeData().hasFormat("application/x-gamepiece"):
      event.acceptProposedAction()

  def dropEvent(self, event):
    if event.mimeData().hasFormat("application/x-gamepiece"):
      pos = event.scenePos()
      if self.selected_item is not None:
        self.selected_item.setPos(pos)
