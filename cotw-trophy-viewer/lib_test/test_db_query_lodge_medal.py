import os
import sys
import unittest

from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge_and_medal(self):
        queryAndHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(queryAndHirsh)
        self.assertEqual(1, len(trophyAnimals))

    def test_db_trophyAnimals_query_lodge_or_medal(self):
        queryOrHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "or",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(queryOrHirsh)
        self.assertEqual(8, len(trophyAnimals))


