import os
import sys
import unittest

from lib.model.animal_type import AnimalType
from lib.model.medal import Medal
from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestAllAnimalsFunctions(unittest.TestCase):

    def test_db_trophyAnimals_all_animals(self):
        query = \
            {
                "lodges": [],
                "reserves": [],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(125, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_reserve(self):
        query = \
            {
                "lodges": [],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(10, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_diamond(self):
        query = \
            {
                "lodges": [],
                "reserves": [],
                "medals": [0],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(114, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_diamond_hirsch(self):
        query = \
            {
                "lodges": [],
                "reserves": [0], # hirsch
                "medals": [0], # diamond, one
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(9, len(trophyAnimals))
        self.assertEqual(Medal.DIAMOND, list(filter(lambda a: a.type == AnimalType.RED_DEER, trophyAnimals))[0].medal)

    def test_db_trophyAnimals_all_animals_gold_hirsch(self):
        query = \
            {
                "lodges": [],
                "reserves": [0], # hirsch
                "medals": [1], # gold, many
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(10, len(trophyAnimals))
        self.assertEqual(Medal.GOLD, list(filter(lambda a: a.type == AnimalType.FALLOW_DEER, trophyAnimals))[0].medal)
        self.assertEqual(Medal.GOLD, list(filter(lambda a: a.type == AnimalType.FALLOW_DEER, trophyAnimals))[1].medal)