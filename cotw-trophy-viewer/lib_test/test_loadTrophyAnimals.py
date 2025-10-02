import unittest

import numpy as np

from lib.load.loader import Loader
from lib.model.animal_type import AnimalType
from lib.model.lodge_type import LodgeType
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH


class TestLoadTrophyAnimalsFunctions(unittest.TestCase):

    def test_loadTrophyAnimals(self):
        trophyAnimals = Loader(paths=Paths(FIXTURES_PATH / 'trophy_lodges_adf')).load_trophy_animals()

        self.assertEqual(len(trophyAnimals), 36)

        testAnimal = \
        list(filter(lambda a: a.type == AnimalType.SALTWATER_CROCODILE and a.weight == 1064.090087890625, trophyAnimals))[0]

        self.assertEqual(testAnimal.weight, 1064.090087890625)
        self.assertEqual(testAnimal.gender, 1)
        self.assertEqual(testAnimal.rating, 1068.0112)
        self.assertEqual(testAnimal.medal, Medal.DIAMOND)
        self.assertEqual(testAnimal.difficulty, 0.9627677202224731)
        self.assertEqual(testAnimal.datetime, '1756497993')
        self.assertEqual(testAnimal.furType, 1)
        self.assertEqual(testAnimal.lodge.lodgeId, np.uint32(2))
        self.assertEqual(testAnimal.lodge.lodgeType, LodgeType.SASEKA_SAFARI)
        self.assertEqual(testAnimal.lodge.lodgeTypeId, 1)
        self.assertEqual(testAnimal.reserve, Reserve.EMERALD_COAST)

    def test_loadTrophyAnimalsNames(self):
        trophyAnimals = Loader(paths=Paths(FIXTURES_PATH / 'trophy_lodges_adf')).load_trophy_animals()

        self.assertTrue(list(filter(lambda a: a.type == AnimalType.EU_RABBIT, trophyAnimals)))

        self.assertTrue(list(filter(lambda a: a.type == AnimalType.EASTERN_GREY_KANGAROO, trophyAnimals)))

        self.assertTrue(list(filter(lambda a: a.type == AnimalType.WILD_TURKEY, trophyAnimals)))

        self.assertTrue(list(filter(lambda a: a.type == AnimalType.ROCKYMOUNTAIN_ELK, trophyAnimals)))
