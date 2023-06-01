#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from typing import NoReturn
from unittest import TestCase

from visualchess import Rank


class TestRank(TestCase):

  def test_str(self) -> NoReturn:
    self.assertEqual(str(Rank.rank0), '1')
    self.assertEqual(str(Rank.rank7), '8')

  def test_getitem(self) -> NoReturn:
    self.assertEqual(Rank.find(1), Rank.rank0)
    self.assertEqual(Rank.find('1'), Rank.rank0)

  def test_getitem_error(self) -> NoReturn:
    with self.assertRaises(TypeError):
      Rank.find(1.0)
    with self.assertRaises(KeyError):
      Rank.find('11')

  def test__getFromInt(self) -> NoReturn:
    self.assertEqual(Rank._getFromInt(1), Rank.rank0)
    with self.assertRaises(IndexError):
      Rank._getFromInt(9)

  def test__getFromStr(self) -> NoReturn:
    self.assertEqual(Rank._getFromStr('1'), Rank.rank0)
    with self.assertRaises(KeyError):
      Rank._getFromStr('11')
