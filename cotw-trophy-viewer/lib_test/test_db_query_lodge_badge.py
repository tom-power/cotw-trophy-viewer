import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge_and_badge(self):
        lodgeOneAndHirsh = \
            {
                "lodges": [2],
                "reserves": [],
                "ratings": [2],
                "animals": [],
                "reservesAndOr": "and",
                "ratingsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOneAndHirsh)
        self.assertEqual(1, len(trophyAnimals))

    def test_db_trophyAnimals_query_lodge_or_animal(self):
        lodgeOneOrHirsh = \
            {
                "lodges": [2],
                "reserves": [],
                "ratings": [2],
                "animals": [],
                "reservesAndOr": "and",
                "ratingsAndOr": "or",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOneOrHirsh)
        self.assertEqual(8, len(trophyAnimals))


