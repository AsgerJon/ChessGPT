"""AudioWidget is responsible for sound effects"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from icecream import ic

from PySide6.QtWidgets import QWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudioDevice, \
  QMediaDevices
from worktoy.core import maybe
from worktoy.stringtools import stringList

from visualchess import Settings
from workstyle import CoreWidget

ic.configureOutput(includeContext=True)


class _SpeakerProperties(CoreWidget):
  """AudioWidget is responsible for sound effects
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def getOutputDeviceByName(deviceName: str = None) -> QAudioDevice:
    """Returns the first instance of QAudioDevice having deviceName in its
    description."""
    deviceName = maybe(deviceName, Settings.deviceName)
    if not isinstance(deviceName, str):
      raise TypeError
    for device in QMediaDevices.audioOutputs():
      if deviceName in device.description():
        return device
    raise NameError('Unable to find an output device named: %s!' %
                    deviceName)

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self._player = None
    self._speaker = None
    self._device = None

  def _createDevice(self) -> NoReturn:
    """Creator-function for device"""
    self._device = self.getOutputDeviceByName(Settings.deviceName)

  def getDevice(self, **kwargs) -> QAudioDevice:
    """Getter-function for audio output device"""
    if self._device is None:
      if kwargs.get('_recursion', None) is not None:
        raise RecursionError
      self._createDevice()
      return self.getDevice(_recursion=True)
    if isinstance(self._device, QAudioDevice):
      return self._device
    raise TypeError

  def _createSpeaker(self) -> NoReturn:
    """Creator-function for speaker"""
    self._speaker = QAudioOutput()

  def getSpeaker(self) -> QAudioOutput:
    """Getter-function for speaker"""
    if self._player is None:
      self._createSpeaker()
      self._speaker.setDevice(self.getDevice())
      return self.getSpeaker()
    if isinstance(self._player, QAudioOutput):
      return self._speaker
    raise TypeError

  def _createPlayer(self) -> NoReturn:
    """Creator-function for player"""
    self._player = QMediaPlayer()

  def getPlayer(self) -> QMediaPlayer:
    """Getter-function for player"""
    if self._player is None:
      self._player = self._createPlayer()
      self._player.setAudioOutput(self._player)
      return self.getPlayer()
    if isinstance(self._player, QMediaPlayer):
      return self._player
    raise TypeError


class Speaker(_SpeakerProperties):
  """Sound Effect widget"""

  def __init__(self, *args, **kwargs) -> None:
    _SpeakerProperties.__init__(self, *args, **kwargs)
