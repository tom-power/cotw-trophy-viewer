import os
import sys
import unittest

from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_medal(self):
        query = \
            {
                "lodges": [],
                "reserves": [],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(5, len(trophyAnimals))

    def test_db_trophyAnimals_query_medal_and_reserve(self):
        query = \
            {
                "lodges": [],
                "reserves": [16],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(2, len(trophyAnimals))
