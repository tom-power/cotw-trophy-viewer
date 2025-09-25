import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestAllPresetsFunctions(unittest.TestCase):

    def test_db_preset(self):
        diamondChecklist = \
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

        presets = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').preset(1)
        self.assertEqual(diamondChecklist, presets)

    def test_db_presets(self):
        presets = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data').presets()
        self.assertEqual({1: 'diamond checklist'}, presets)
