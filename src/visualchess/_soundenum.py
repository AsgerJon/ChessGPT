"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
import os
from typing import Never, NoReturn

from PySide6.QtCore import QUrl
from icecream import ic
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from visualchess import SoundBoard

ic.configureOutput(includeContext=True)


class Sound(IntEnum):
  """Each sound effect is defined here as Sound enum"""

  @staticmethod
  def getSoundPath() -> str:
    """Getter-function for sound path"""
    root = os.getenv('CHESSGPT')
    there = os.path.join(
      *stringList('src, visualchess, chesspieces, sounds'))
    return os.path.join(root, there)

  MOVE = 0
  SLIDE = 1
  WHOOSH = 2

  def getFileName(self) -> str:
    """Getter-function for fileName"""
    baseName = self.name.lower()
    return '%s.wav' % (baseName)

  def setFileName(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('fileName')

  def getFilePath(self, ) -> str:
    """Getter-function for file path"""
    return os.path.join(self.getSoundPath(), self.getFileName())

  def setFilePath(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('soundPath')

  def getUrl(self) -> QUrl:
    """Getter-function for the filePath as QUrl"""
    return QUrl.fromLocalFile(self.getFilePath())

  def setUrl(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('url')

  def _createSoundBoard(self) -> NoReturn:
    """Creates the media player"""
    setattr(self, '_soundBoard', SoundBoard())
    _soundBoard = getattr(self, '_soundBoard')
    _soundBoard.onPlay(self.handlePlay)
    self._loadSound()

  def _loadSound(self, ) -> NoReturn:
    """Loads the sound file"""
    _soundBoard = self.getSoundBoard()
    if not isinstance(_soundBoard, SoundBoard):
      raise TypeError
    _soundBoard.setSource(self.getUrl())

  def getSoundBoard(self) -> SoundBoard:
    """Getter-function for player"""
    if getattr(self, '_soundBoard', None) is None:
      self._createSoundBoard()
      return self.getSoundBoard()
    _soundBoard = getattr(self, '_soundBoard', None)
    if isinstance(_soundBoard, SoundBoard):
      return _soundBoard
    raise TypeError

  def handlePlay(self) -> NoReturn:
    """Handler function for the play signal emitted by the sound board."""
    deviceName = self.getSoundBoard().getDevice()
    print('%s tried to play a sound!' % self)
    print('%s uses sound device: %s' % (self, deviceName))

  def play(self) -> NoReturn:
    """Triggers the sound effect"""
    self.getSoundBoard().play()

  def __str__(self, ) -> str:
    """String representation"""
    msg = """Sound effect: %s!""" % (self.name.capitalize())
    return msg

  def __repr__(self) -> str:
    """Code Representation"""
    return """SoundEffect.%s""" % self.name
