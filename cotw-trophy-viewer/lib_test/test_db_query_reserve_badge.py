import os
import sys
import unittest

from lib.db.db import Db
from lib.load.loader import Loader
from lib.hub import Hub
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_medal(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOne)
        self.assertEqual(5, len(trophyAnimals))

    def test_db_trophyAnimals_query_medal_and_reserve(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [16],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOne)
        self.assertEqual(2, len(trophyAnimals))
