import os
import sys
import unittest

from lib.db.db import Db
from lib.load.loader import Loader
from lib.ui.hub import Hub
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge_and_medal(self):
        lodgeOneAndHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOneAndHirsh)
        self.assertEqual(1, len(trophyAnimals))

    def test_db_trophyAnimals_query_lodge_or_medal(self):
        lodgeOneOrHirsh = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [2],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "or",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOneOrHirsh)
        self.assertEqual(8, len(trophyAnimals))


