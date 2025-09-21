import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_badge(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [],
                "ratings": [2],
                "animals": [],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(5, len(trophyAnimals))

    def test_db_trophyAnimals_query_badge_and_reserve(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [16],
                "ratings": [2],
                "animals": [],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(2, len(trophyAnimals))
