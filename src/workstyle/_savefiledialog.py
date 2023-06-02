#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QPixmap


class SavePixmapDialog(QFileDialog):
  """
  Subclass of QFileDialog for saving QPixmap as png file
  """

  def __init__(self, parent=None):
    """
    Initialize SavePixmapDialog

    :param parent: parent QWidget
    """
    super(SavePixmapDialog, self).__init__(parent)

  def savePixmap(self, pixmap: QPixmap, fileName: str = None):
    """
    Open a dialog and save QPixmap as a png file

    :param pixmap: QPixmap object to be saved
    :param fileName: Optional file name for saving
    """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    if not fileName:
      fileName, _ = QFileDialog.getSaveFileName(self,
                                                "Save Image",
                                                "",
                                                "PNG Files (*.png)",
                                                options=options)
    if fileName:
      pixmap.save(fileName, 'PNG')
      return fileName
    return None
