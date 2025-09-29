import os
import sys
import unittest

from lib.db.db import Db
from lib.load.loader import Loader
from lib.ui.hub import Hub
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestDbFunctions(unittest.TestCase):

    def test_db_trophyAnimals_query_lodge(self):
        lodgeOne = \
            {
                "lodges": [1],
                "reserves": [],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOne)
        self.assertEqual(4, len(trophyAnimals))

    def test_db_trophyAnimals_query_hirsch(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOne)
        self.assertEqual(4, len(trophyAnimals))

    def test_db_trophyAnimals_query_and(self):
        lodgeOneAndHirsh = \
            {
                "lodges": [1],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOneAndHirsh)
        self.assertEqual(2, len(trophyAnimals))

    def test_db_trophyAnimals_query_or(self):
        lodgeOneOrHirsh = \
            {
                "lodges": [1],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "or",
                "medalsAndOr": "and",
                "animalsAndOr": "and"
            }

        trophyAnimals = Hub(Db(db_path=FIXTURES_PATH / 'data'), Loader(loadPath=FIXTURES_PATH)).trophyAnimals(lodgeOneOrHirsh)
        self.assertEqual(6, len(trophyAnimals))


