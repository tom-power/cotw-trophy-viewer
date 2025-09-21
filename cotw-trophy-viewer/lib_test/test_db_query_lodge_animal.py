import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge_and_animal(self):
        lodgeOneAndHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [],
                "animals": [1511159411],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOneAndHirsh)
        self.assertEqual(3, len(trophyAnimals))

    def test_db_trophyAnimals_query_lodge_or_animal(self):
        lodgeOneOrHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [],
                "animals": [1511159411],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "or"
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOneOrHirsh)
        self.assertEqual(6, len(trophyAnimals))


