import unittest

from lib.model.difficulty import Difficulty


class TestDifficultyFunctions(unittest.TestCase):

    def test_getDifficultyName_trivial(self):
        self.assertEqual("1 - TRIVIAL", Difficulty.getDifficultyName(0.1))

    def test_getDifficultyName_fabled(self):
        self.assertEqual("10 - FABLED", Difficulty.getDifficultyName(0.996))
