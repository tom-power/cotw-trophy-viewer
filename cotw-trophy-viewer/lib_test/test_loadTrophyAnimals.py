import unittest

import numpy as np

from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.model.trophyanimal import TrophyAnimal
from lib_test.fixtures import FIXTURES_PATH


class TestLoadTrophyAnimalsFunctions(unittest.TestCase):

    def test_loadTrophyAnimals(self):
        trophyAnimals = loadTrophyAnimals(FIXTURES_PATH)

        self.assertEqual(len(trophyAnimals), 36)
        testAnimal = list(filter(lambda a: a.type == "FALLOW DEER", trophyAnimals))[0]

        self.assertIsInstance(testAnimal, TrophyAnimal)
        self.assertEqual(testAnimal.weight, 90)
        self.assertEqual(testAnimal.gender, 1)
        self.assertEqual(testAnimal.score, 215.97388)
        self.assertEqual(testAnimal.rating, 1)
        self.assertEqual(testAnimal.difficulty, 0.39767796)
        self.assertEqual(testAnimal.datetime, '1738269517')
        self.assertEqual(testAnimal.furType, 9)
        self.assertEqual(testAnimal.lodge, np.uint32(0))
        self.assertEqual(testAnimal.reserve, np.uint32(0))
