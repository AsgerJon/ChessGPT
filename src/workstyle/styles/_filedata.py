"""FileData holds file data for the application centrally"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QSize, QPointF, QSizeF
from PySide6.QtGui import QPixmap, QColor
from worktoy.core import maybe
from worktoy.typetools import CallMeMaybe
from worktoy.waitaminute import ReadOnlyError


class Data:
  """Class providing the dot"""

  def __init__(self,
               name: str,
               defVal: object = None,
               type_: type = None,
               **kwargs) -> None:
    self._name = name
    self._value = defVal
    self._type = type_
    if (self._value is None) ^ (self._type is None):
      if self._value is not None:
        self._type = maybe(self._type, type(self._value))
    self._allowGet = kwargs.get('allowGet', True)
    self._allowSet = kwargs.get('allowSet', True)
    self._allowDel = kwargs.get('allowDel', False)

  def getValue(self) -> object:
    """Explicit getter function allowing subclasses to reimplement"""
    if self._allowGet:
      return self._value
    raise ReadOnlyError('%s' % self._name)

  def setValue(self, value: object) -> NoReturn:
    """Explicit setter function allowing subclasses to reimplement"""
    if self._allowSet:
      self._value = value
      return
    raise ReadOnlyError('%s' % self._name)

  def delValue(self, ) -> NoReturn:
    """Explicit deleter function allowing subclasses to reimplement"""
    if self._allowDel:
      self._value = None
      return
    raise ReadOnlyError('%s' % self._name)

  def __get__(self, instance, owner) -> object:
    """Getter"""
    return self.getValue()

  def __set__(self, instance, value) -> NoReturn:
    """Setter"""
    self._value = value

  def __del__(self, *args) -> NoReturn:
    """Deleter"""
    self._value = None

  def __getattr__(self, key: str) -> object:
    """Passes on to the wrapped object"""
    return getattr(self._value, key)


class Factory(Data):
  """Subclass reimplementing the getter function"""

  def __init__(self, *args, **kwargs) -> None:
    Data.__init__(self, *args, **kwargs)
    self._function = None

  def __call__(self, *args, **kwargs) -> object:
    """When first called it should receive a function which is the invoked
    on future calls"""
    if self._function is None:
      self._function = args[0]
      if not isinstance(self._function, CallMeMaybe):
        raise TypeError
      return self
    return self._invokeFunction(*args, **kwargs)

  def _invokeFunction(self, *args, **kwargs) -> object:
    """Function invocation"""
    return self._function(*args, **kwargs)

  def getValue(self) -> object:
    """Reimplementation of getter function"""
    return self._invokeFunction()


class FileData:
  """FileData holds file data for the application centrally
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  SCALE = 1600
  _envName = 'CHESSGPT'
  _imageFormat = 'png'
  _imageName = 'chess_gpt'
  _imageSize = QSize(SCALE, SCALE)

  envName = Data('envName', _envName, str, )
  imageFormat = Data('imageFormat', _imageFormat, str)
  imageName = Data('imageName', _imageName, str)
  imageSize = Data('imageSize', _imageSize, QSize)
  imageWidth = Data('imageWidth', imageSize.width(), int)
  imageHeight = Data('imageWidth', imageSize.height(), int)

  @classmethod
  def getImageFilePath(cls) -> str:
    """Getter-function for the image file path"""
    dirName = os.getenv(cls.envName)
    return os.path.join(dirName,
                        '%s.%s' % (cls._imageName, cls._imageFormat), )

  @classmethod
  def createPixmap(cls) -> QPixmap:
    """Creator-function for pix map"""
    pix = QPixmap(cls.imageWidth, cls.imageHeight)
    pix.fill(QColor(0, 0, 0, 0, ))
    return pix

  @classmethod
  def getScale(cls) -> float:
    """Getter-function for scale"""
    return cls.SCALE

  @classmethod
  def getSize(cls) -> QSizeF:
    """Getter-function for the size at the current scale"""
    return QSizeF(cls.SCALE, cls.SCALE)


class BoardDims:
  """Board dimensions"""

  bezelPixels = 32 * (FileData.getScale() / 400)
  marginLeft = 16 * (FileData.getScale() / 400)
  marginTop = 16 * (FileData.getScale() / 400)
  marginRight = 16 * (FileData.getScale() / 400)
  marginBottom = 16 * (FileData.getScale() / 400)
  gridPixels = 3 * (FileData.getScale() / 400)
  cornerRadiusX = 8 * (FileData.getScale() / 400)
  cornerRadiusY = 8 * (FileData.getScale() / 400)
  origin = QPointF(0, 0)


class StaticView:
  """Dimensions relative to the board size. """

  bezel = 32 / 400
  marginLeft = 16 / 400
  marginTop = 16 / 400
  marginRight = 16 / 400
  marginBottom = 16 / 400
  gridPixels = 3 / 400
  innerGrid = 3 / 400
  outerGrid = 5 / 400
  cornerRadiusX = 8 / 400
  cornerRadiusY = 8 / 400
