import os
import sys
import unittest

from lib.model.animal_type import AnimalType
from lib.model.medal import Medal
from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestAllAnimalsFunctions(unittest.TestCase):

    def test_db_trophyAnimals_all_animals_great_one(self):
        query = \
            {
                "lodges": [],
                "reserves": [],
                "medals": [5],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(8, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_great_one_hirsch(self):
        query = \
            {
                "lodges": [],
                "reserves": [0],
                "medals": [5],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(4, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_great_one_te_aw(self):
        query = \
            {
                "lodges": [],
                "reserves": [10],
                "medals": [5],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(2, len(trophyAnimals))
        self.assertEqual(Medal.GREAT_ONE, list(filter(lambda a: a.type == AnimalType.FALLOW_DEER, trophyAnimals))[0].medal)