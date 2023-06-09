#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QImage, QPixmap, QColor, QPainterPath, \
  QFont
from PySide6.QtCore import Qt, QRectF


class MyWidget(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.header_image = QImage("headerimage.png")
    self.profile_image = QImage("profil2021.jpg")
    self.title_text = "How to pip install YourStuff!"

    # Check if the images have been loaded correctly
    if self.header_image.isNull():
      print("Failed to load header image.")
    if self.profile_image.isNull():
      print("Failed to load profile image.")

  def paintEvent(self, event):
    if self.header_image.isNull() or self.profile_image.isNull():
      # Don't attempt to paint if any of the images couldn't be loaded
      return

    painter = QPainter(self)

    # Draw the header image
    painter.drawImage(0,
                      0,
                      self.header_image.scaled(self.width(), self.height()))

    # Apply color overlay
    painter.setBrush(QColor(0, 0, 0, 127))  # Semi-transparent black
    painter.drawRect(self.rect())

    # Draw the title text
    painter.setFont(QFont("Arial", 20, QFont.Bold))
    painter.setPen(QColor(Qt.white))
    painter.drawText(QRectF(0, 0, self.width(), self.height()),
                     Qt.AlignCenter,
                     self.title_text)

    # Draw the profile image (make it circular)
    path = QPainterPath()
    path.addEllipse(0,
                    0,
                    self.profile_image.width(),
                    self.profile_image.height())
    rounded_profile_image = QImage(self.profile_image.size(),
                                   QImage.Format_ARGB32)
    rounded_profile_image.fill(Qt.transparent)

    profile_painter = QPainter(rounded_profile_image)
    profile_painter.setClipPath(path)
    profile_painter.drawImage(0, 0, self.profile_image)
    profile_painter.end()

    # Determine position for the profile image (Top-right corner,
    # with padding)
    padding = 10
    profile_x = self.width() - rounded_profile_image.width() - padding
    profile_y = padding

    # Draw the rounded profile image
    painter.drawImage(profile_x, profile_y, rounded_profile_image)

  def resizeEvent(self, event):
    self.update()  # Trigger a repaint whenever the widget is resized
