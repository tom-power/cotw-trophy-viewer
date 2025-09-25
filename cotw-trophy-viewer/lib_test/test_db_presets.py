import os
import sys
import unittest

from lib.db.db import Db
from lib_test.fixtures import FIXTURES_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestAllPresetsFunctions(unittest.TestCase):

    def setUp(self):
        self.db = Db(loadPath=FIXTURES_PATH, db_path=FIXTURES_PATH / 'data')
        self.db.presetClear()
        self.db.presetInit()

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

        presets_list = self.db.presets()
        diamond_preset_id = None
        for preset_id, name in presets_list.items():
            if name == "diamond checklist":
                diamond_preset_id = preset_id
                break

        self.assertIsNotNone(diamond_preset_id)
        presets = self.db.preset(diamond_preset_id)
        self.assertEqual(diamondChecklist, presets)

    def test_db_presets(self):
        presets = self.db.presets()
        self.assertEqual(1, len(presets))
        self.assertIn('diamond checklist', presets.values())

    def test_db_preset_add(self):
        test_query = {
            "lodges": [1, 2],
            "reserves": [3, 4],
            "medals": [1, 2],
            "animals": [5, 6],
            "reservesAndOr": "or",
            "medalsAndOr": "or",
            "animalsAndOr": "or",
            "allAnimals": False
        }

        self.db.presetAdd("test preset", test_query)

        presets = self.db.presets()
        self.assertEqual(2, len(presets))
        self.assertIn('test preset', presets.values())

        test_preset_id = None
        for preset_id, name in presets.items():
            if name == "test preset":
                test_preset_id = preset_id
                break

        self.assertIsNotNone(test_preset_id)
        retrieved_query = self.db.preset(test_preset_id)
        self.assertEqual(test_query, retrieved_query)

    def test_db_preset_add_duplicate_name(self):
        test_query1 = {"medals": [1], "allAnimals": True}
        test_query2 = {"medals": [2], "allAnimals": False}

        self.db.presetAdd("duplicate name", test_query1)
        initial_presets = self.db.presets()

        self.db.presetAdd("duplicate name", test_query2)
        final_presets = self.db.presets()

        self.assertEqual(len(initial_presets), len(final_presets))

        preset_id = None
        for preset_id, name in final_presets.items():
            if name == "duplicate name":
                break

        self.assertIsNotNone(preset_id)
        retrieved_query = self.db.preset(preset_id)
        self.assertEqual(test_query1, retrieved_query)
