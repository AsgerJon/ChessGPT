"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from icecream import ic
from worktoy.waitaminute import ReadOnlyError

from workside.audio import Sound

ic.configureOutput(includeContext=True)


class ChessAudio:
  """Sound Settings"""

  def __init__(self, ) -> None:
    self._soundAllowedCapture = Sound.whoosh
    self._soundAllowedMove = Sound.move
    self._soundIllegalCapture = Sound.error
    self._soundIllegalMove = Sound.right2jail_rightaway
    self._soundCancelMove = Sound.error
    self._soundForbidden = Sound.error
    self._soundGainFocus = Sound.slide

  def _getAllowedCapture(self) -> Sound:
    """Getter-function for allowed capture sound"""
    return self._soundAllowedCapture

  def _getAllowedMove(self) -> Sound:
    """Getter-function for allowed move sound"""
    return self._soundAllowedMove

  def _getIllegalCapture(self) -> Sound:
    """Getter-function for illegal capture sound"""
    return self._soundIllegalCapture

  def _getIllegalMove(self) -> Sound:
    """Getter-function for illegal move sound"""
    return self._soundIllegalMove

  def _getCancelMove(self) -> Sound:
    """Getter-function for cancel move sound"""
    return self._soundCancelMove

  def _getForbidden(self) -> Sound:
    """Getter-function for sound indicating a general forbidden action"""
    return self._soundForbidden

  def _getFocusGain(self) -> Sound:
    """Getter-function for sound indicating a general forbidden action"""
    return self._soundGainFocus

  def _noAcc(self, *args) -> Never:
    """Illegal Accessor"""
    raise ReadOnlyError('General Illegal Access attempted!')

  soundAllowedCapture = property(_getAllowedCapture, _noAcc, _noAcc)
  soundAllowedMove = property(_getAllowedMove, _noAcc, _noAcc)
  soundIllegalCapture = property(_getIllegalCapture, _noAcc, _noAcc)
  soundIllegalMove = property(_getIllegalMove, _noAcc, _noAcc)
  soundCancelMove = property(_getCancelMove, _noAcc, _noAcc)
  soundForbidden = property(_getForbidden, _noAcc, _noAcc)
  soundGainFocus = property(_getFocusGain, _noAcc, _noAcc)
