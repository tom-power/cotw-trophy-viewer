import os
import sys
import unittest

from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge(self):
        query = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(4, len(trophyAnimals))

    def test_db_trophyAnimals_query_hirsch(self):
        query = \
            {
                "lodges": [],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(query)
        self.assertEqual(4, len(trophyAnimals))

    def test_db_trophyAnimals_query_and(self):
        queryAndHirsh = \
            {
                "lodges": [1],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(queryAndHirsh)
        self.assertEqual(2, len(trophyAnimals))

    def test_db_trophyAnimals_query_or(self):
        queryOrHirsh = \
            {
                "lodges": [1],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "or",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = getDb().trophyAnimals(queryOrHirsh)
        self.assertEqual(6, len(trophyAnimals))


