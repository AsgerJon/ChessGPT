#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from unittest import TestCase

from visualchess import File


class TestFile(TestCase):
  def test_str(self):
    self.assertEqual(str(File.A), 'A')
    self.assertEqual(str(File.H), 'H')

  def test_getitem(self):
    self.assertEqual(File.find(1), File.A)
    self.assertEqual(File.find('A'), File.A)
    with self.assertRaises(KeyError):
      File.find(1.0)
    with self.assertRaises(KeyError):
      File.find('AA')

  def test_getFromInt(self):
    self.assertEqual(File._getFromInt(1), File.A)
    with self.assertRaises(IndexError):
      File._getFromInt(-1)

  def test_getFromStr(self):
    self.assertEqual(File._getFromStr('A'), File.A)
    with self.assertRaises(KeyError):
      File._getFromStr('AA')
