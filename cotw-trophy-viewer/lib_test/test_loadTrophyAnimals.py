import unittest

import numpy as np

from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.model.animalType import AnimalType
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophyanimal import TrophyAnimal
from lib_test.fixtures import FIXTURES_PATH


class TestLoadTrophyAnimalsFunctions(unittest.TestCase):

    def test_loadTrophyAnimals(self):
        trophyAnimals = loadTrophyAnimals(FIXTURES_PATH)

        self.assertEqual(len(trophyAnimals), 36)
        testAnimal = list(filter(lambda a: a.type == AnimalType.FALLOW_DEER, trophyAnimals))[0]

        self.assertIsInstance(testAnimal, TrophyAnimal)
        self.assertEqual(testAnimal.weight, 90)
        self.assertEqual(testAnimal.gender, 1)
        self.assertEqual(testAnimal.rating, 215.97388)
        self.assertEqual(testAnimal.medal, Medal.GOLD)
        self.assertEqual(testAnimal.difficulty, 0.39767796)
        self.assertEqual(testAnimal.datetime, '1738269517')
        self.assertEqual(testAnimal.furType, 9)
        self.assertEqual(testAnimal.lodge, np.uint32(1))
        self.assertEqual(testAnimal.reserve, Reserve.HIRSCHFELDEN)

        testAnimal = \
        list(filter(lambda a: a.type == AnimalType.SALTWATER_CROCODILE and a.weight == 1064.090087890625, trophyAnimals))[0]

        self.assertIsInstance(testAnimal, TrophyAnimal)
        self.assertEqual(testAnimal.weight, 1064.090087890625)
        self.assertEqual(testAnimal.gender, 1)
        self.assertEqual(testAnimal.rating, 1068.0112)
        self.assertEqual(testAnimal.medal, Medal.DIAMOND)
        self.assertEqual(testAnimal.difficulty, 0.9627677202224731)
        self.assertEqual(testAnimal.datetime, '1756497993')
        self.assertEqual(testAnimal.furType, 1)
        self.assertEqual(testAnimal.lodge, np.uint32(3))
        self.assertEqual(testAnimal.reserve, Reserve.EMERALD_COAST)

    def test_loadTrophyAnimalsNames(self):
        trophyAnimals = loadTrophyAnimals(FIXTURES_PATH)

        testAnimal = list(filter(lambda a: a.type == AnimalType.EU_RABBIT, trophyAnimals))[0]
        self.assertIsInstance(testAnimal, TrophyAnimal)

        testAnimal = list(filter(lambda a: a.type == AnimalType.EASTERN_GREY_KANGAROO, trophyAnimals))[0]
        self.assertIsInstance(testAnimal, TrophyAnimal)

        testAnimal = list(filter(lambda a: a.type == AnimalType.WILD_TURKEY, trophyAnimals))[0]
        self.assertIsInstance(testAnimal, TrophyAnimal)

        testAnimal = list(filter(lambda a: a.type == AnimalType.ROCKYMOUNTAIN_ELK, trophyAnimals))[0]
        self.assertIsInstance(testAnimal, TrophyAnimal)
