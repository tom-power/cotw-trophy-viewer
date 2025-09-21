import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge(self):
        lodgeOne = \
            {
                "lodges": [1],
                "reserves": [],
                "ratings": [],
                "animals": [],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(3, len(trophyAnimals))

    def test_db_trophyAnimals_query_hirsch(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [0],
                "ratings": [],
                "animals": [],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(4, len(trophyAnimals))

    def test_db_trophyAnimals_query_and(self):
        lodgeOneAndHirsh = \
            {
                "lodges": [1],
                "reserves": [0],
                "ratings": [],
                "animals": [],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOneAndHirsh)
        self.assertEqual(2, len(trophyAnimals))

    def test_db_trophyAnimals_query_or(self):
        lodgeOneOrHirsh = \
            {
                "lodges": [1],
                "reserves": [0],
                "ratings": [],
                "animals": [],
                "reservesAndOr": "or",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOneOrHirsh)
        self.assertEqual(5, len(trophyAnimals))


