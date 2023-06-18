"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import Never, NoReturn

from PySide6.QtCore import QUrl, QObject
from PySide6.QtWidgets import QApplication
from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from moreworktoy import Iterify
from workside.audio import SoundEffect, Settings
from workside.widgets import CoreWidget

ic.configureOutput(includeContext=True)


class _SoundProperties(Iterify):
  """Class containing the properties for the sound class"""

  @staticmethod
  def _getSoundPath() -> str:
    """Getter-function for sound path"""
    fromEnv = os.getenv('WORKSIDE_AUDIO_FILES')
    if fromEnv:
      return fromEnv
    root = os.getenv('CHESSGPT')
    there = os.path.join(
      *stringList('src, visualchess, chesspieces, sounds'))
    return os.path.join(root, there)

  def __init__(self, *args, **kwargs) -> None:
    parent = CoreWidget.parseParent(*args, **kwargs)
    self._parent = maybe(parent, QApplication.instance())
    self._name = None
    self._soundEffect = None
    self._fileName = None
    self._url = None

  def _getParent(self) -> CoreWidget:
    """Getter-function for the parent widget"""
    if isinstance(self._parent, QObject):
      return self._parent
    return QApplication.instance()

  def _createSoundEffect(self) -> NoReturn:
    """Creator-function for the sound effect"""
    self._soundEffect = SoundEffect(
      self._getParent(), Settings.deviceName)
    self._soundEffect.setLoopCount(1)
    self._soundEffect.setSource(self.url)

  def _getSoundEffect(self) -> SoundEffect:
    """Getter-function for the sound effect"""
    if self._soundEffect is None:
      self._createSoundEffect()
      return self._getSoundEffect()
    if isinstance(self._soundEffect, SoundEffect):
      return self._soundEffect
    raise TypeError

  def _setSoundEffect(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('sound effect')

  def _getName(self) -> str:
    """Getter-function for the name"""
    return self._name

  def _setName(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('name')

  def _getFileName(self) -> str:
    """Getter-function for fileName"""
    baseName = self._getName().lower()
    return '%s.wav' % (baseName)

  def _setFileName(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('fileName')

  def _getFilePath(self, ) -> str:
    """Getter-function for file path"""
    return os.path.join(self._getSoundPath(), self._getFileName())

  def _setFilePath(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('filePath')

  def _createUrl(self) -> NoReturn:
    """Creator function for the url"""
    self._url = QUrl.fromLocalFile(self._getFilePath())

  def _getUrl(self) -> QUrl:
    """Getter-function for url pointing to the sound file"""
    if self._url is None:
      self._createUrl()
      return self._getUrl()
    if isinstance(self._url, QUrl):
      return self._url
    raise TypeError

  def _setUrl(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('url')

  name = property(_getName, _setName, _setName)
  fileName = property(_getFileName, _setFileName, _setFileName)
  url = property(_getUrl, _setUrl, _setUrl)
  filePath = property(_getFilePath, _setFilePath, _setFilePath)
  effect = property(_getSoundEffect, _setSoundEffect, _setSoundEffect, )


class Sound(_SoundProperties):
  """Each sound effect is defined here as Sound enum"""

  @classmethod
  def createAll(cls, *args) -> NoReturn:
    """Collects all wave files in given folder. Defaults to folder given
    by soundPath"""
    folder = cls._getSoundPath()
    if not isinstance(folder, str):
      raise TypeError
    for file in os.listdir(folder):
      name_, fileExt = os.path.splitext(file)
      if fileExt.replace('.', '') == 'wav':
        instance = cls(name_)
        setattr(cls, name_, instance)

  @staticmethod
  def _parseArguments(*args, **kwargs) -> str:
    """Parses the arguments to name"""
    nameKeys = stringList('name, title, instanceName')
    name, args, kwargs = extractArg(str, nameKeys, *args, **kwargs)
    if isinstance(name, str):
      return name
    raise TypeError

  @classmethod
  def __old__(cls, *args, **kwargs) -> NoReturn:
    """Attempts to find an existing instance"""
    name = cls._parseArguments(*args, **kwargs)
    instances = getattr(cls, '__instances__', None)
    if instances is None:
      raise ValueError
    for sound in instances:
      if sound.name == name:
        return sound
    return None

  def __init__(self, *args, **kwargs) -> None:
    _SoundProperties.__init__(self, *args, **kwargs)
    self._name = self._parseArguments(*args, **kwargs)

  def _loadSound(self, ) -> NoReturn:
    """Loads the sound file"""
    self.effect.setSource(self.url)

  def handlePlay(self) -> NoReturn:
    """Handler function for the play signal emitted by the sound board."""

  def play(self) -> NoReturn:
    """Triggers the sound effect"""
    self.effect.play()

  def __str__(self, ) -> str:
    """String representation"""
    msg = """Sound effect: %s!""" % (self.name.capitalize())
    return msg

  def __repr__(self) -> str:
    """Code Representation"""
    return """SoundEffect.%s""" % self.name

  def __call__(self) -> NoReturn:
    """Triggers the sound effect"""
    self.effect.play()
