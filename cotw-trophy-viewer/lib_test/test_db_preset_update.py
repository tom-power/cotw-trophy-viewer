import os
import sys
import unittest

from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestPresetRemoveFunctions(unittest.TestCase):

    def setUp(self):
        self.db = getDb()

    def tearDown(self):
        for p in self.db.presets():
            self.db.presetRemove(p)

    def test_db_preset_update(self):
        test_query_name = "preset to update"
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
        test_query_updated_name = 'preset updated'
        test_query_updated = {
            "lodges": [1],
            "reserves": [3, 4],
            "medals": [1],
            "animals": [5, 6],
            "reservesAndOr": "or",
            "medalsAndOr": "or",
            "animalsAndOr": "or",
            "allAnimals": False
        }

        self.db.presetAdd(test_query_name, test_query)
        presets_before = self.db.presets()
        self.assertEqual(3, len(presets_before))
        presetId = [k for k, v in presets_before.items() if v == test_query_name][0]
        self.assertEqual(test_query, self.db.preset(presetId))
        self.assertIn(test_query_name, presets_before.values())

        self.db.presetUpdate(presetId, test_query_updated_name, test_query_updated)

        presets_after_update = self.db.presets()
        self.assertEqual(3, len(presets_after_update))
        self.assertNotIn(test_query_name, presets_after_update.values())
        self.assertIn(test_query_updated_name, presets_after_update.values())
        self.assertEqual(test_query_updated, self.db.preset(presetId))
