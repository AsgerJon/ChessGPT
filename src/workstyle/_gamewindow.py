#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class DraggableItem(QGraphicsItem):
  def __init__(self, rect, color, text, parent=None):
    super().__init__(parent)
    self.rect = rect
    self.color = color
    self.text = text
    self.setFlags(
      QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

  def boundingRect(self):
    return self.rect

  def paint(self, painter, option, widget):
    painter.setPen(QPen(Qt.black, 2))
    painter.setBrush(QBrush(self.color))
    painter.drawRect(self.rect)
    painter.drawText(self.rect, Qt.AlignCenter, self.text)

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.setCursor(Qt.ClosedHandCursor)

  def mouseMoveEvent(self, event):
    if event.buttons() == Qt.LeftButton:
      mimeData = QMimeData()
      byteArray = QByteArray()
      dataStream = QDataStream(byteArray, QIODevice.WriteOnly)
      dataStream << self.rect << self.color << self.text
      mimeData.setData('application/x-qgraphicsitem', byteArray)
      drag = QDrag(event.widget())
      drag.setMimeData(mimeData)
      drag.setHotSpot(event.pos().toPoint())
      drag.exec_(Qt.MoveAction)
      self.setCursor(Qt.OpenHandCursor)

  def mouseReleaseEvent(self, event):
    self.setCursor(Qt.OpenHandCursor)


class GraphicsView(QGraphicsView):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setDragMode(QGraphicsView.RubberBandDrag)
    self.setScene(QGraphicsScene(self))
    self.setSceneRect(0, 0, 400, 300)
    self.setRenderHint(QPainter.Antialiasing)

  def dragEnterEvent(self, event):
    event.acceptProposedAction()

  def dragMoveEvent(self, event):
    event.acceptProposedAction()

  def dropEvent(self, event):
    if event.mimeData().hasFormat('application/x-qgraphicsitem'):
      itemData = event.mimeData().data('application/x-qgraphicsitem')
      dataStream = QDataStream(itemData, QIODevice.ReadOnly)
      rect = QRectF()
      color = QColor()
      text = QString()
      dataStream >> rect >> color >> text
      item = DraggableItem(rect, color, text)
      item.setPos(event.scenePos())
      self.scene().addItem(item)
      event.acceptProposedAction()

  def startDrag(self, item):
    itemData = QMimeData()
    byteArray = QByteArray()
    dataStream = QDataStream(byteArray, QIODevice.WriteOnly)
    dataStream << item.boundingRect() << item.color << item.text
    itemData.setData('application/x-qgraphicsitem', byteArray)
    drag = QDrag(self)
    drag.setMimeData(itemData)
    drag.exec_(Qt.MoveAction)


class GameWindow(QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle('Drag and Drop Example')
    self.setGeometry(100, 100, 400, 300)
    self.view = GraphicsView(self)
    self.setCentralWidget(self.view)

    rect = QRectF(0, 0, 80, 60)
    color = QColor(Qt.blue)
    text = 'Drag me!'
    item = DraggableItem(rect, color, text)
    item.setPos(100, 100)
    self.view.scene().addItem(item)
    self.view.startDrag(item)


if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec()
