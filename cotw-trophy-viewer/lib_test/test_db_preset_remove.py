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

    def test_db_preset_remove(self):
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

        self.db.presetAdd("test preset to remove", test_query)

        presets_before = self.db.presets()
        self.assertEqual(3, len(presets_before))
        self.assertIn('test preset to remove', presets_before.values())

        preset_id_to_remove = None
        for preset_id, name in presets_before.items():
            if name == "test preset to remove":
                preset_id_to_remove = preset_id
                break

        self.assertIsNotNone(preset_id_to_remove)

        self.db.presetRemove(preset_id_to_remove)

        presets_after = self.db.presets()
        self.assertEqual(2, len(presets_after))
        self.assertNotIn('test preset to remove', presets_after.values())
        self.assertIn('layton lake lodge todo', presets_after.values())
