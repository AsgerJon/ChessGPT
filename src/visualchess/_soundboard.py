"""SoundBoard subclasses QMediaPlayer providing a class with slots named as
given by the SoundEnum instances."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Signal, Slot
from PySide6.QtMultimedia import QMediaPlayer, QMediaDevices, QAudioDevice, \
  QAudioOutput
from icecream import ic
from worktoy.core import maybe
from worktoy.typetools import CallMeMaybe

from visualchess import Settings
from workstyle import CoreWidget

ic.configureOutput(includeContext=True)


class _SoundPlayerProperties(QMediaPlayer):
  """_SoundPlayerProperties contains properties used by SoundBoard.
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
    msg = """Unable to find an output device named: %s!"""
    raise NameError(msg % deviceName)

  def __init__(self, *args, **kwargs) -> None:
    QMediaPlayer.__init__(self, )
    self._device = None
    self._output = None
    self._subscribers = None

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

  def _createOutput(self) -> NoReturn:
    """Creator-function for speaker"""
    self._output = QAudioOutput()

  def getSpeaker(self) -> QAudioOutput:
    """Getter-function for speaker"""
    if self._output is None:
      self._createOutput()
      if isinstance(self._output, QAudioOutput):
        self._output.setDevice(self.getDevice())
        return self.getSpeaker()
      raise TypeError
    if isinstance(self._output, QAudioOutput):
      return self._output
    raise TypeError

  def _createSubscribers(self) -> NoReturn:
    """Creator function for the list of subscribers"""
    self._subscribers = []

  def _getSubscribers(self) -> list[CallMeMaybe]:
    """Getter-function for list of subscribers"""
    if self._subscribers is None:
      self._createSubscribers()
      return self._getSubscribers()
    if isinstance(self._subscribers, list):
      return self._subscribers


class SoundBoard(_SoundPlayerProperties):
  """SoundBoard subclasses QMediaPlayer providing a class with slots
  named as given by the SoundEnum instances.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  alertPlay = Signal()

  def __init__(self, *args, **kwargs) -> None:
    _SoundPlayerProperties.__init__(self, *args, **kwargs)
    self.setAudioOutput(self.getSpeaker())
    self.alertPlay.connect(self.alertPlayStrong)

  def onPlay(self, slot: CallMeMaybe) -> NoReturn:
    """Adds slot to list of strong references alerted explicitly by the
    alertPlay signal."""
    self._getSubscribers().append(slot)

  def alertPlayStrong(self) -> NoReturn:
    """The following actions are triggered when alert play would be called"""
    for slot in self._getSubscribers():
      slot()

  @Slot()
  def play(self) -> NoReturn:
    """Reimplementation emitting the alertPlay signal before activating"""
    self.alertPlay.emit()
    QMediaPlayer.play(self)

  def __str__(self, ) -> str:
    """String Representation"""
    deviceName = self.getDevice()
    msg = """SoundBoard instance using device: %s""" % deviceName
    return msg

  def __repr__(self, ) -> str:
    """Code Representation"""
    return """SoundBoard()"""
