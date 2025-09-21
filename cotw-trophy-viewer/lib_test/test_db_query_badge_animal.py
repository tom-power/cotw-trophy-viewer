import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_fallow(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [],
                "ratings": [],
                "animals": [1511159411],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(6, len(trophyAnimals))

    def test_db_trophyAnimals_query_fallow_and_silver(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [],
                "ratings": [2],
                "animals": [1511159411],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(2, len(trophyAnimals))

    def test_db_trophyAnimals_query_fallow_or_silver(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [],
                "ratings": [2],
                "animals": [1511159411],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "or"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(9, len(trophyAnimals))
