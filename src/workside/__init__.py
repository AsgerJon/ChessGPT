"""WorkSide streamlines your use of PySide6 enabling your access to Qt from
Python!"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import time

from icecream import ic
import builtins

from worktoy.stringtools import stringList
from worktoy.waitaminute import n00bError

original_import = __import__
__all__ = stringList(
  """workside, dialogs, workside.settings, workside.styles, 
  workside.widgets, workside.windows, workside.audio""")


def customImport(name, gls=None, lcs=None, fromlist=(), level=0):
  """Stop using star imports!"""
  if fromlist == ('*',) and name in __all__:
    here = os.path.dirname(os.path.abspath(__file__))
    lyricsPath = os.path.join(here, 'lyrics.txt')
    noobPath = os.path.join(here, 'nooberror.txt')
    with open(lyricsPath, 'r', encoding='utf-8') as f:
      lyrics = f.read().split('\n')
    with open(noobPath, 'r', encoding='utf-8') as f:
      noob = f.read()
    for lyric in lyrics:
      print(lyric)
      time.sleep(0.3)
    raise n00bError(noob)
  return original_import(name, gls, lcs, fromlist, level)


builtins.__import__ = customImport
ic.configureOutput(includeContext=True)
