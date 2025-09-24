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
        self.assertEqual(117, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_reserve(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [0],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(10, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_diamond(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [],
                "medals": [0],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(106, len(trophyAnimals))

    def test_db_trophyAnimals_all_animals_diamond_hirsch(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [0], # hirsch
                "medals": [0], # diamond, one
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(9, len(trophyAnimals))
        self.assertEqual(0, list(filter(lambda a: a.type.animalName() == "RED DEER", trophyAnimals))[0].medal)

    def test_db_trophyAnimals_all_animals_gold_hirsch(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [0], # hirsch
                "medals": [1], # gold, many
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        self.assertEqual(10, len(trophyAnimals))
        self.assertEqual(1, list(filter(lambda a: a.type.animalName() == "FALLOW DEER", trophyAnimals))[0].medal)
        self.assertEqual(1, list(filter(lambda a: a.type.animalName() == "FALLOW DEER", trophyAnimals))[1].medal)

    def test_db_trophyAnimals_all_animals_diamond_emerald(self):
        lodgeOne = \
            {
                "lodges": [],
                "reserves": [16], # emerald
                "medals": [0], # diamond, many
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        trophyAnimals = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').trophyAnimals(lodgeOne)
        # self.assertEqual(9, len(trophyAnimals))
        self.assertEqual(0, list(filter(lambda a: a.type.animalName() == "STUBBLE QUAIL", trophyAnimals))[0].medal)
        self.assertEqual(0, list(filter(lambda a: a.type.animalName() == "BANTENG", trophyAnimals))[0].medal)
