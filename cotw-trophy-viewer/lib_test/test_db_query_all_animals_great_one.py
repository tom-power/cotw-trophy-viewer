import os
import sys
import unittest

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
