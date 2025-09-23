import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestAllAnimalsFunctions(unittest.TestCase):

    def test_db_trophyAnimals_all_animals(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(108, len(trophyAnimals))
