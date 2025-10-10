import os
import sys
import unittest

from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge_and_animal(self):
        queryAndHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [],
                "animals": [1511159411], # FALLOW_DEER = 1511159411  # 0x5a127673
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(queryAndHirsh)
        self.assertEqual(1, len(trophyAnimals))

    def test_db_trophyAnimals_query_lodge_or_animal(self):
        queryOrHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [],
                "animals": [1511159411], # FALLOW_DEER = 1511159411  # 0x5a127673
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "or"
            }

        trophyAnimals = getDb().trophyAnimals(queryOrHirsh)
        self.assertEqual(9, len(trophyAnimals))


